lucide.createIcons();

function showLogoModal() {
  document.getElementById('logoModal').classList.remove('hidden');
}
function hideLogoModal() {
  document.getElementById('logoModal').classList.add('hidden');
}

function togglePassword(fieldId, button) {
  const input = document.getElementById(fieldId);
  const icon = button.querySelector('i');
  const isHidden = input.type === 'password';
  input.type = isHidden ? 'text' : 'password';
  icon.setAttribute('data-lucide', isHidden ? 'eye-off' : 'eye');
  lucide.createIcons();
}

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById('page-transition');
  if (container) {
    container.classList.remove('opacity-0');
    container.classList.add('opacity-100');
  }

  const form = document.getElementById('passwordForm');
  const inputs = Array.from(form.querySelectorAll('input'));
  const submitBtn = document.getElementById('submitBtn');
  const spinner = document.getElementById('spinner');
  const submitText = document.getElementById('submitText');

  inputs.forEach((input, idx) => {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const next = inputs[idx + 1];
        if (next) next.focus();
        else form.requestSubmit();
      }
    });
  });

  form.addEventListener('submit', () => {
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');
    submitText.textContent = 'Updating...';
  });

  document.querySelectorAll('a[href]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (el.target === '_blank' || el.href?.startsWith('http')) return;
      e.preventDefault();
      container.classList.remove('opacity-100');
      container.classList.add('opacity-0');
      setTimeout(() => (window.location.href = el.href), 300);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') hideLogoModal();
  });
});
