lucide.createIcons();

// Fade-in on load
document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('page-transition');
  if (container) {
    container.classList.remove('opacity-0');
    container.classList.add('opacity-100');
  }

  const form = document.getElementById('usernameForm');
  const spinner = document.getElementById('spinner');
  const submitText = document.getElementById('submitText');
  const submitBtn = document.getElementById('submitBtn');

  form.addEventListener('submit', function () {
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');
    submitText.textContent = "Updating...";
  });
});

// Logo Modal Functions
function showLogoModal() {
  document.getElementById('logoModal').classList.remove('hidden');
}
function hideLogoModal() {
  document.getElementById('logoModal').classList.add('hidden');
}

// Close modal on Escape
document.addEventListener('keydown', function (e) {
  if (e.key === "Escape") {
    hideLogoModal();
  }
});
