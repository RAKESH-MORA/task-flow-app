lucide.createIcons();

function togglePassword() {
  const pwd = document.getElementById('password');
  const icon = document.getElementById('toggleIcon');
  if (pwd.type === 'password') {
    pwd.type = 'text';
    icon.setAttribute('data-lucide', 'eye-off');
  } else {
    pwd.type = 'password';
    icon.setAttribute('data-lucide', 'eye');
  }
  lucide.createIcons();
}

function showLogoModal() {
  document.getElementById('logoModal').classList.remove('hidden');
}

function hideLogoModal() {
  document.getElementById('logoModal').classList.add('hidden');
}

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") hideLogoModal();
});

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('page-transition');
  if (container) {
    container.classList.remove('opacity-0');
    container.classList.add('opacity-100');
  }

  const form = document.getElementById('registerForm');
  const inputs = Array.from(form.querySelectorAll('input'));
  const spinner = document.getElementById('spinner');
  const submitText = document.getElementById('submitText');
  const submitBtn = document.getElementById('submitBtn');

  // Navigate between inputs using Enter key
  inputs.forEach((input, idx) => {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const next = inputs[idx + 1];
        if (next) {
          next.focus();
        } else {
          form.requestSubmit();
        }
      }
    });
  });

  // Show spinner on submit
  form.addEventListener('submit', function () {
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');
    submitText.textContent = "Creating...";
  });
});
