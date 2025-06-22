lucide.createIcons();

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('page-transition');
  container?.classList.remove('opacity-0');
  container?.classList.add('opacity-100');

  const form = document.getElementById('verifyForm');
  const spinner = document.getElementById('spinner');
  const submitText = document.getElementById('submitText');
  const submitBtn = document.getElementById('submitBtn');

  if (form) {
    form.addEventListener('submit', function () {
      submitBtn.disabled = true;
      spinner.classList.remove('hidden');
      submitText.textContent = "Verifying...";
    });
  }

  // Countdown (3 minutes)
  const timerEl = document.getElementById("timer");
  let duration = 180;
  const countdown = setInterval(() => {
    const minutes = String(Math.floor(duration / 60)).padStart(2, '0');
    const seconds = String(duration % 60).padStart(2, '0');
    if (timerEl) timerEl.textContent = `${minutes}:${seconds}`;
    if (--duration < 0) {
      clearInterval(countdown);
      if (timerEl) timerEl.textContent = "Expired";
    }
  }, 1000);
});

function showLogoModal() {
  document.getElementById('logoModal').classList.remove('hidden');
}

function hideLogoModal() {
  document.getElementById('logoModal').classList.add('hidden');
}

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") hideLogoModal();
});
