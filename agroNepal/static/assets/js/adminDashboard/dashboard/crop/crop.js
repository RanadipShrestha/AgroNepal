function openEditModal(id, name, desc) {
  document.getElementById("edit_crop_id").value = id;
  document.getElementById("edit_crop_name").value = name;
  document.getElementById("edit_crop_desc").value = desc === "None" ? "" : desc;
  document.getElementById("editModal").style.display = "flex";
}

// Custom Delete Modal Logic
document.addEventListener("DOMContentLoaded", function () {
  const deleteModal = document.getElementById("deleteCropModal");
  const cancelDeleteBtn = document.getElementById("cancelDeleteCropBtn");
  const deleteBtns = document.querySelectorAll(".delete-crop-btn");

  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      document.getElementById("deleteCropId").value = this.getAttribute("data-cropid");
      document.getElementById("deleteCropName").textContent = this.getAttribute("data-cropname");
      deleteModal.classList.add("active");
    });
  });

  cancelDeleteBtn.addEventListener("click", function () {
    deleteModal.classList.remove("active");
  });

  // Add Confirmation Logic
  const confirmAddModal = document.getElementById("confirmAddModal");
  const confirmEditModal = document.getElementById("confirmEditModal");

  document.getElementById("triggerAddConfirmBtn").addEventListener("click", function () {
    const form = document.getElementById("addCropForm");
    if (form.checkValidity()) {
      confirmAddModal.classList.add("active");
    } else {
      form.reportValidity();
    }
  });

  document.getElementById("cancelAddBtn").addEventListener("click", function () {
      confirmAddModal.classList.remove("active");
    });

  document.getElementById("confirmAddBtn").addEventListener("click", function () {
      document.getElementById("addCropForm").submit();
    });

  // Edit Confirmation Logic
  document.getElementById("triggerEditConfirmBtn").addEventListener("click", function () {
      const form = document.getElementById("editCropForm");
      if (form.checkValidity()) {
        confirmEditModal.classList.add("active");
      } else {
        form.reportValidity();
      }
    });

  document.getElementById("cancelEditBtn").addEventListener("click", function () {
      confirmEditModal.classList.remove("active");
    });

  document.getElementById("confirmEditBtn").addEventListener("click", function () {
      document.getElementById("editCropForm").submit();
    });

  window.onclick = function (event) {
    if (event.target == document.getElementById("addModal")) {
      document.getElementById("addModal").style.display = "none";
    }
    if (event.target == document.getElementById("editModal")) {
      document.getElementById("editModal").style.display = "none";
    }
    if (event.target === deleteModal) {
      deleteModal.classList.remove("active");
    }
    if (event.target === confirmAddModal) {
      confirmAddModal.classList.remove("active");
    }
    if (event.target === confirmEditModal) {
      confirmEditModal.classList.remove("active");
    }
  };
});

    document.addEventListener("DOMContentLoaded", function () {
      const toasts = document.querySelectorAll(".toast-message");
      toasts.forEach((toast) => {
        setTimeout(() => {
          toast.classList.add("hide");
          setTimeout(() => toast.remove(), 400);
        }, 3500);
      });
    });