lucide.createIcons();

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('page-transition');
  if (container) {
    container.classList.remove('opacity-0');
    container.classList.add('opacity-100');
  }
});

function showLogoModal() {
  document.getElementById('logoModal').classList.remove('hidden');
}

function hideLogoModal() {
  document.getElementById('logoModal').classList.add('hidden');
}

function showConfirmModal() {
  document.getElementById('confirmModal').classList.remove('hidden');
}

function hideConfirmModal() {
  document.getElementById('confirmModal').classList.add('hidden');
}

function submitDelete() {
  const btn = document.getElementById('confirmDeleteBtn');
  const spinner = document.getElementById('deleteSpinner');
  const text = document.getElementById('confirmDeleteText');

  btn.disabled = true;
  spinner.classList.remove('hidden');
  text.textContent = 'Deleting...';

  setTimeout(() => {
    document.getElementById('deleteForm').submit();
  }, 300);
}

function togglePassword(fieldId, button) {
  const input = document.getElementById(fieldId);
  const icon = button.querySelector('i');

  if (input.type === 'password') {
    input.type = 'text';
    icon.setAttribute('data-lucide', 'eye-off');
  } else {
    input.type = 'password';
    icon.setAttribute('data-lucide', 'eye');
  }

  lucide.createIcons();
}

document.addEventListener('keydown', function (e) {
  if (e.key === "Escape") {
    hideLogoModal();
    hideConfirmModal();
  }
});
