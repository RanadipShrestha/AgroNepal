document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert, index) => {
    setTimeout(
      () => {
        alert.style.animation = "slideOut 0.4s ease-out";
        setTimeout(() => {
          alert.remove();
        }, 400);
      },
      5000 + index * 200,
    ); // Stagger dismissal if multiple alerts
  });
});

// Manual close function
function closeAlert(alertId) {
    const alert = document.getElementById(alertId);
    if (alert) {
        alert.style.animation = 'slideOut 0.4s ease-out';
        setTimeout(() => {
            alert.remove();
        }, 400);
    }
}