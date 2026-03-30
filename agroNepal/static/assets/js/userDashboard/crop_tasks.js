function cropTaskOpenModal(userCropId, cropName) {
  document.getElementById("cropTaskModalCropName").textContent = cropName;
  document.getElementById("cropTaskHideForm").action =`/userDashboard/crop-tasks/hide/${userCropId}/`;
  document.getElementById("cropTaskConfirmModal").classList.add("active");
}

function cropTaskCloseModal() {
  document.getElementById("cropTaskConfirmModal").classList.remove("active");
}

document
  .getElementById("cropTaskConfirmModal")
  .addEventListener("click", function (e) {
    if (e.target === this) cropTaskCloseModal();
  });

setTimeout(function cropTaskDismissAlerts() {
  document.querySelectorAll(".crop-task-alert-message").forEach(function (el) {
    el.style.opacity = "0";
    el.style.transform = "translateX(50px)";
    setTimeout(function () {
      el.remove();
    }, 400);
  });
}, 3000);
