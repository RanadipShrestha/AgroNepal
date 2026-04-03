document.addEventListener("DOMContentLoaded", function () {
  const confirmModal = document.getElementById("edit-event-confirmModal");
  const eventForm = document.getElementById("edit-event-eventForm");

  document
    .getElementById("edit-event-triggerConfirmBtn")
    .addEventListener("click", function () {
      if (eventForm.checkValidity()) {
        confirmModal.classList.add("edit-event-active");
      } else {
        eventForm.reportValidity();
      }
    });

  document
    .getElementById("edit-event-cancelBtn")
    .addEventListener("click", function () {
      confirmModal.classList.remove("edit-event-active");
    });

  document
    .getElementById("edit-event-confirmBtn")
    .addEventListener("click", function () {
      eventForm.submit();
    });

  window.addEventListener("click", function (event) {
    if (event.target === confirmModal) {
      confirmModal.classList.remove("edit-event-active");
    }
  });
});
