document.addEventListener('DOMContentLoaded', function () {
  // --- Selectors ---
  const addCropBtn = document.getElementById("addCropBtn");
  const addCropModal = document.getElementById("addCropModal");
  const editCropModal = document.getElementById("editCropModal");
  const deleteModal = document.getElementById("deleteModal");
  const confirmationModal = document.getElementById("confirmationModal");
  
  const addForm = document.getElementById("addCropForm");
  const editForm = document.getElementById("editCropForm");

  // --- Modal Openers (Direct IDs) ---
  if (addCropBtn) {
    addCropBtn.addEventListener("click", () => {
      if (addCropModal) addCropModal.style.display = "block";
    });
  }

  // --- Event Delegation for Crop Cards (Edit and Delete) ---
  document.addEventListener("click", function (event) {
    const target = event.target;

    // Edit Button Detection (using closest for better accuracy)
    const editBtn = target.closest(".edit-crop-btn");
    if (editBtn) {
       console.log("Edit button clicked. Data attributes:", editBtn.dataset);
      try {
        const userCropId = editBtn.getAttribute("data-user-crop-id");
        const cropId = editBtn.getAttribute("data-crop-id");
        const plantedDate = editBtn.getAttribute("data-planted-date");
        const notes = editBtn.getAttribute("data-notes");

        const inputs = {
          userCropIdField: document.getElementById("editUserCropId"),
          cropSelectField: document.getElementById("editCropSelect"),
          dateInputField: document.getElementById("editCropDateInput"),
          noteInputField: document.getElementById("editCropNoteInput")
        };

        // Populate fields
        if (inputs.userCropIdField) inputs.userCropIdField.value = userCropId || "";
        if (inputs.cropSelectField) inputs.cropSelectField.value = cropId || "";
        if (inputs.dateInputField) inputs.dateInputField.value = plantedDate || "";
        if (inputs.noteInputField) inputs.noteInputField.value = notes || "";

        if (editCropModal) {
          editCropModal.style.display = "block";
        } else {
          console.error("Edit modal element not found.");
        }
      } catch (err) {
        console.error("Error opening edit modal:", err);
      }
    }

    // Delete Button Detection
    const deleteBtn = target.closest(".delete-crop-btn");
    if (deleteBtn) {
      const cropId = deleteBtn.dataset.cropId;
      const cropName = deleteBtn.dataset.cropName;
      
      const idInput = document.getElementById("deleteCropId");
      const nameSpan = document.getElementById("deleteCropName");
      
      if (idInput) idInput.value = cropId;
      if (nameSpan) nameSpan.textContent = cropName;
      if (deleteModal) deleteModal.style.display = "block";
    }

    // Close Buttons
    if (target.classList.contains("close-btn") || target.id === "closeModalBtn" || target.id === "closeEditModalBtn") {
      const modal = target.closest(".modal");
      if (modal) {
        modal.style.display = "none";
        if (modal === addCropModal && addForm) addForm.reset();
      }
    }

    // Cancel Buttons
    if (target.id === "cancelAddCropBtn") {
      if (confirmationModal) confirmationModal.style.display = "none";
      if (addCropModal) addCropModal.style.display = "block";
    }
    if (target.id === "cancelDeleteBtn") {
      if (deleteModal) deleteModal.style.display = "none";
    }
  });

  // --- Add Crop Form Logic (with Confirmation) ---
  const submitBtn = document.getElementById("submitBtn");
  const confirmAddCropBtn = document.getElementById("confirmAddCropBtn");

  if (submitBtn) {
    submitBtn.addEventListener("click", () => {
      if (addCropModal) addCropModal.style.display = "none";
      if (confirmationModal) confirmationModal.style.display = "block";
    });
  }

  if (confirmAddCropBtn) {
    confirmAddCropBtn.addEventListener("click", () => {
      if (confirmationModal) confirmationModal.style.display = "none";
      if (addForm) addForm.submit();
    });
  }

  // --- Click Outside to Close ---
  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
      if (event.target === addCropModal && addForm) addForm.reset();
    }
  });

  // --- Auto-Dismiss Alerts ---
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add("fade-out");
      setTimeout(() => alert.remove(), 600);
    }, 4000); 
  });
});
