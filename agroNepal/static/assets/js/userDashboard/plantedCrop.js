document.addEventListener('DOMContentLoaded', function () {
  const addCropBtn = document.getElementById("addCropBtn");
  const addCropModal = document.getElementById("addCropModal");
  const confirmationModal = document.getElementById("confirmationModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const form = document.getElementById("addCropForm");
  const submitBtn = document.getElementById("submitBtn");
  const confirmBtn = document.getElementById("confirmBtn");
  const cancelBtn = document.getElementById("cancelBtn");

  addCropBtn.addEventListener("click", function () {
    addCropModal.style.display = "block";
  });

  closeModalBtn.addEventListener("click", function () {
    addCropModal.style.display = "none";
    form.reset();
  });

  submitBtn.addEventListener("click", function () {
    addCropModal.style.display = "none";
    confirmationModal.style.display = "block";
  });
  
  // Handle confirm button
  confirmBtn.addEventListener("click", function () {
    confirmationModal.style.display = "none";
    form.submit();
  });

  // Handle cancel button
  cancelBtn.addEventListener("click", function () {
    confirmationModal.style.display = "none";
    addCropModal.style.display = "block";
  });

  // Close modals when clicking outside
  window.addEventListener("click", function (event) {
    if (event.target === addCropModal) {
      addCropModal.style.display = "none";
      form.reset();
    }
    if (event.target === confirmationModal) {
      confirmationModal.style.display = "none";
      addCropModal.style.display = "block";
    }
  });
})

//Planted crop delete garana JS
document.addEventListener("DOMContentLoaded", function () {
  const deleteModal = document.getElementById("deleteModal");
  const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");

  document.querySelectorAll(".delete-crop-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      document.getElementById("deleteCropId").value = this.dataset.cropId;
      document.getElementById("deleteCropName").textContent =
        this.dataset.cropName;
      deleteModal.style.display = "block";
    });
  });

  cancelDeleteBtn.addEventListener("click", function () {
    deleteModal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === deleteModal) {
      deleteModal.style.display = "none";
    }
  });
});


//Messages hurur autmatic hide garana JS
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add("fade-out");
      setTimeout(() => {
        alert.remove();
      }, 600);
    }, 3000); 
  });
});

