
# ✅ Task Flow — Flask-Based Task Management System

## 📌 Overview

**Task Flow** is a fully functional task management web application built with **Flask**, designed to streamline personal productivity through intuitive task handling and real-time notifications. The application features a modern, responsive frontend styled with **Tailwind CSS**, closely mirroring the **React + shadcn/ui** design system, and supports both light and dark themes.

## 🔧 Features

### 🔐 User Authentication
- Secure **registration**, **login**, and **logout**
- **Email verification via OTP** during registration  
  - Max 3 attempts allowed  
  - Re-registration restricted for 24 hours on failure
- **Change password** and **delete account** options available from the settings panel

### 🗂️ Task Management
- Create, view, update, modify, and delete tasks
- Each task includes:
  - Title
  - Description (supports wrapped content)
  - Priority (Low, Medium, High)
  - Due Date and Time (calendar + time picker; past dates restricted)
  - Status (Pending, In Progress, Completed)
- Status can be toggled directly from the dashboard

### 🔍 Search & Filter
- Filter tasks by:
  - Title (search by keyword)
  - Due Date
  - Status (Pending / In Progress / Completed)

### 🔔 Notifications
- Task reminders for upcoming or due tasks
- UI indicators for overdue tasks

### 🌗 UI & UX
- Built with **Tailwind CSS** and fully responsive
- Forms and modals styled with a blurred white background
- Inputs include icons from **Lucide Icons**
- Clean dashboard with:
  - Add Task modal
  - Edit/Delete/Toggle controls
  - Search/filter bar on the right side

## 🏗️ Tech Stack

| Component        | Technology                |
|------------------|----------------------------|
| Backend          | Flask (Python)             |
| Database         | SQLAlchemy (SQLite/MySQL)  |
| Frontend         | HTML + Tailwind CSS        |
| Icons            | Lucide Icons               |
| Email Service    | Flask-Mail (OTP handling)  |
| Date/Time Picker | Flatpickr / native support |

## 🚀 Installation

```bash
git clone https://github.com/RAKESH-MORA/task-flow-app.git
cd flask-task-flow-app
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask run
```

> ⚠️ Configure environment variables (email, secret key, etc.) in `.env` or a `config.py` file.

## 📁 Project Structure

```
task-flow/
├── static/
│   └── css, js, icons
├── templates/
│   └── *.html (dashboard, login, register, etc.)
├── app.py
├── models.py
├── forms.py
├── utils/
│   └── email_otp.py, notification.py
├── requirements.txt
└── README.md
```

## ✅ To-Do / Future Enhancements

- [ ] Task category/tags
- [ ] Admin dashboard
- [ ] Progressive Web App (PWA) support
- [ ] Push notifications
- [ ] Multi-user collaboration

## 🧑‍💼 Author

**Rakesh**  
Full-stack developer passionate about productivity tools and intuitive UI/UX design.
