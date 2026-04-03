document.addEventListener("DOMContentLoaded", function () {
  const confirmModal = document.getElementById("add_event-confirmModal");
  const eventForm = document.getElementById("add_event-eventForm");

  document
    .getElementById("add_event-triggerConfirmBtn")
    .addEventListener("click", function () {
      if (eventForm.checkValidity()) {
        confirmModal.classList.add("active");
      } else {
        eventForm.reportValidity();
      }
    });

  document
    .getElementById("add_event-cancelBtn")
    .addEventListener("click", function () {
      confirmModal.classList.remove("active");
    });

  document
    .getElementById("add_event-confirmBtn")
    .addEventListener("click", function () {
      eventForm.submit();
    });

  window.addEventListener("click", function (event) {
    if (event.target === confirmModal) {
      confirmModal.classList.remove("active");
    }
  });
});
