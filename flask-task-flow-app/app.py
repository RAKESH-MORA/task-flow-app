from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import random
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_app_password'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# In-memory store for OTPs (consider using Redis or DB for production)
otp_store = {}

# Prevent caching of protected pages
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Decorator for login required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade="all, delete")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    priority = db.Column(db.String(20), nullable=False, default='Normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    due_time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def is_due_soon(self):
        now = datetime.now()
        due = datetime.combine(self.due_date, self.due_time)
        return 0 <= (due - now).total_seconds() <= 300 and self.status != 'Completed'

# Utility to send OTP
def send_otp(email, otp):
    subject = "Your OTP Code"
    body = f"Your verification code is: {otp}"
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message)
    except Exception as e:
        print("Failed to send email:", e)

# Routes
@app.route('/')
@login_required
def home():
    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found. Please log in again.", "danger")
        session.pop('user_id', None)
        return redirect(url_for('login'))

    now = datetime.now()
    user_tasks = Task.query.filter_by(user_id=user.id).all()
    for task in user_tasks:
        due_datetime = datetime.combine(task.due_date, task.due_time)
        if due_datetime < now and task.status not in ['Completed', 'Pending']:
            task.status = 'Pending'
    db.session.commit()

    search_query = request.args.get('search', '').strip()
    base_query = Task.query.filter_by(user_id=user.id)

    if search_query:
        try:
            search_date = datetime.strptime(search_query, "%Y-%m-%d").date()
            search_time = datetime.strptime(search_query, "%H:%M").time()
            tasks = base_query.filter(
                (Task.title.ilike(f'%{search_query}%')) |
                (Task.status.ilike(f'%{search_query}%')) |
                (Task.priority.ilike(f'%{search_query}%')) |
                (Task.due_date == search_date) |
                (Task.due_time == search_time)
            ).all()
        except ValueError:
            tasks = base_query.filter(
                (Task.title.ilike(f'%{search_query}%')) |
                (Task.status.ilike(f'%{search_query}%')) |
                (Task.priority.ilike(f'%{search_query}%')) |
                (Task.due_date.cast(db.String).ilike(f'%{search_query}%')) |
                (Task.due_time.cast(db.String).ilike(f'%{search_query}%'))
            ).all()
    else:
        tasks = []

    tasks_all = base_query.order_by(Task.created_at.desc()).all()
    tasks_due_soon = [task for task in tasks_all if task.is_due_soon()]

    return render_template('dashboard.html', tasks=tasks, tasks_all=tasks_all, tasks_due_soon=tasks_due_soon, user=user, datetime=datetime)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'warning')
            return redirect(url_for('register'))

        otp = random.randint(100000, 999999)
        otp_store[email] = {
            'otp': str(otp),
            'attempts': 0,
            'created_at': datetime.utcnow()
        }
        send_otp(email, otp)
        session['temp_user'] = {'name': name, 'email': email, 'password': generate_password_hash(password)}
        return redirect(url_for('verify_email'))

    return render_template('register.html')

@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    temp_user = session.get('temp_user')
    if not temp_user:
        flash("No registration data found.", "danger")
        return redirect(url_for('register'))

    email = temp_user['email']
    if request.method == 'POST':
        entered_otp = request.form['code']
        record = otp_store.get(email)

        if not record:
            flash("OTP expired or invalid.", "danger")
            return redirect(url_for('register'))

        if datetime.utcnow() - record['created_at'] > timedelta(minutes=3):
            del otp_store[email]
            flash("OTP expired. Please register again.", "danger")
            return redirect(url_for('register'))

        if record['attempts'] >= 3:
            flash("Maximum attempts exceeded. Try again after 24 hours.", "danger")
            return redirect(url_for('register'))

        if record['otp'] != entered_otp:
            record['attempts'] += 1
            flash("OTP didn't match. Please try again.", "danger")
            return redirect(url_for('verify_email'))

        new_user = User(name=temp_user['name'], email=email, password=temp_user['password'])
        db.session.add(new_user)
        db.session.commit()
        del otp_store[email]
        session.pop('temp_user', None)
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('verify_email.html', email=email)

# ✅ NEW: Resend OTP route
@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    temp_user = session.get('temp_user')
    if not temp_user:
        flash("Session expired. Please register again.", "danger")
        return redirect(url_for('register'))

    email = temp_user['email']
    otp = random.randint(100000, 999999)
    otp_store[email] = {
        'otp': str(otp),
        'attempts': 0,
        'created_at': datetime.utcnow()
    }
    send_otp(email, otp)
    flash('OTP has been resent to your email.', 'info')
    return redirect(url_for('verify_email'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User not found. Please register first.', 'danger')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'warning')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        flash('Login successful.', 'success')
        return redirect(url_for('login', success=1))

    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form.get('status', 'Pending')
    priority = request.form.get('priority', 'Normal')
    due_date = datetime.strptime(request.form['due_date'], "%Y-%m-%d").date()
    due_time = datetime.strptime(request.form['due_time'], "%H:%M").time()

    new_task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        due_time=due_time,
        user_id=session['user_id']
    )

    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form['status']
    db.session.commit()
    flash('Task status updated.', 'success')
    return redirect(url_for('home'))

@app.route('/modify/<int:task_id>', methods=['POST'])
@login_required
def modify_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.title = request.form['title']
    task.description = request.form['description']
    task.status = request.form['status']
    task.priority = request.form['priority']
    task.due_date = datetime.strptime(request.form['due_date'], "%Y-%m-%d").date()
    task.due_time = datetime.strptime(request.form['due_time'], "%H:%M").time()
    db.session.commit()
    flash('Task updated successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not check_password_hash(user.password, old_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'warning')
            return redirect(url_for('change_password'))

        if check_password_hash(user.password, new_password):
            flash('This password is currently in use. Choose a different one.', 'warning')
            return redirect(url_for('change_password'))

        user.password = generate_password_hash(new_password)
        db.session.commit()
        session.clear()
        flash('Password changed successfully. Please log in again.', 'success')
        return redirect(url_for('login'))

    return render_template('change_password.html', user=user)

@app.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        new_name = request.form['new_name'].strip()

        if not new_name:
            flash('Name cannot be empty.', 'warning')
            return redirect(url_for('change_username'))

        user.name = new_name
        db.session.commit()
        flash('Username updated successfully.', 'success')
        return redirect(url_for('change_username'))

    return render_template('change_username.html', user=user)

@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        password = request.form['password']

        if not check_password_hash(user.password, password):
            flash('Invalid password. Account not deleted.', 'danger')
            return redirect(url_for('delete_user'))

        db.session.delete(user)
        db.session.commit()
        session.clear()
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('delete_user.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)