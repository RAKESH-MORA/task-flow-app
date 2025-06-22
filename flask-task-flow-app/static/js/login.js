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

  // Fade-out transition on form/button click
  document.querySelectorAll('a[href], button[type="submit"]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (el.target === '_blank' || el.href?.startsWith('http')) return;
      const container = document.getElementById('page-transition');
      if (container) {
        e.preventDefault();
        container.classList.remove('opacity-100');
        container.classList.add('opacity-0');
        setTimeout(() => {
          if (el.tagName === 'A') {
            window.location.href = el.href;
          } else {
            el.closest('form').submit();
          }
        }, 300);
      }
    });
  });

  // Enter key navigation
  const form = document.getElementById('loginForm');
  const inputs = Array.from(form.querySelectorAll('input'));

  inputs.forEach((input, idx) => {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const next = inputs[idx + 1];
        if (next) {
          next.focus();
        } else {
          form.submit();
        }
      }
    });
  });
});
