document.addEventListener("DOMContentLoaded", function () {
  const confirmModal = document.getElementById("confirmModal");
  const blogForm = document.getElementById("blogForm");

  const triggerConfirmBtn = document.getElementById("blogTriggerConfirmBtn");
  if (triggerConfirmBtn) {
    triggerConfirmBtn.addEventListener("click", function () {
      if (blogForm.checkValidity()) {
        confirmModal.classList.add("active");
      } else {
        blogForm.reportValidity();
      }
    });
  }

  const cancelBtn = document.getElementById("cancelBtn");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", function () {
      confirmModal.classList.remove("active");
    });
  }

  const confirmBtn = document.getElementById("confirmBtn");
  if (confirmBtn) {
    confirmBtn.addEventListener("click", function () {
      blogForm.submit();
    });
  }

  window.addEventListener("click", function (event) {
    if (event.target === confirmModal) {
      confirmModal.classList.remove("active");
    }
  });
});
