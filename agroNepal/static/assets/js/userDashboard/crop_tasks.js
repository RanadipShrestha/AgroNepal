// ============================================
//  CROP TASK – All identifiers prefixed: cropTask
// ============================================

/**
 * Opens the confirmation modal for hiding/deleting a crop's tasks.
 * @param {string} userCropId - The unique ID of the user's crop instance.
 * @param {string} cropName   - The display name of the crop.
 */
function cropTaskOpenModal(userCropId, cropName) {
  document.getElementById("cropTaskModalCropName").textContent = cropName;
  document.getElementById("cropTaskHideForm").action =
    `/userDashboard/crop-tasks/hide/${userCropId}/`;
  document.getElementById("cropTaskConfirmModal").classList.add("active");
}

/**
 * Closes the confirmation modal.
 */
function cropTaskCloseModal() {
  document.getElementById("cropTaskConfirmModal").classList.remove("active");
}

// Close modal when clicking on the overlay backdrop
document
  .getElementById("cropTaskConfirmModal")
  .addEventListener("click", function (e) {
    if (e.target === this) cropTaskCloseModal();
  });

// Auto-dismiss alert toasts after 3 seconds
setTimeout(function cropTaskDismissAlerts() {
  document.querySelectorAll(".crop-task-alert-message").forEach(function (el) {
    el.style.opacity = "0";
    el.style.transform = "translateX(50px)";
    setTimeout(function () {
      el.remove();
    }, 400);
  });
}, 3000);
