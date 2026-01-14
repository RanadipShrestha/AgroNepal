// Simple reusable JS for both Expense and Sales pages

document.addEventListener("DOMContentLoaded", function () {
  // Get all modals
  const addModal = document.querySelector(".modal");
  const allModals = document.querySelectorAll(".modal");

  let confirmCallback = null;

  // Show modal
  function showModal(modal) {
    modal.style.display = "block";
  }

  // Hide modal
  function hideModal(modal) {
    modal.style.display = "none";
  }

  // Close modals when clicking X button
  document.querySelectorAll(".close-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const modal = this.closest(".modal");
      hideModal(modal);
    });
  });

  // Open Add modal (works for both Add Expense and Add Sale)
  const addButtons = document.querySelectorAll("#addExpenseBtn, #addSaleBtn");
  addButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const modal = document.querySelector("#addExpenseModal, #addSaleModal");
      showModal(modal);
    });
  });

  // Submit Add form with confirmation
  const submitButtons = document.querySelectorAll(
    "#submitExpenseBtn, #submitSaleBtn"
  );
  submitButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const form = this.closest("form");
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const confirmModal = document.getElementById("confirmationModal");
      const confirmText = document.getElementById("confirmationText");
      confirmText.textContent = "Are you sure you want to save this?";
      confirmCallback = () => form.submit();
      showModal(confirmModal);
    });
  });

  // Edit buttons
  document.querySelectorAll(".edit-expense-sale-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const editModal = document.querySelector(
        "#editExpenseModal, #editSaleModal"
      );

      // For Expense
      if (this.dataset.expenseId) {
        document.getElementById("editExpenseId").value = this.dataset.expenseId;
        document.getElementById("edit_amount").value = this.dataset.amount;
        document.getElementById("edit_spend_date").value =
          this.dataset.spendDate;
        document.getElementById("edit_note").value = this.dataset.note || "";
      }

      // For Sale
      if (this.dataset.saleId) {
        document.getElementById("editSaleId").value = this.dataset.saleId;
        document.getElementById("edit_amount").value = this.dataset.amount;
        document.getElementById("edit_quantity").value =
          this.dataset.quantity || "";
        document.getElementById("edit_sale_date").value = this.dataset.saleDate;
        document.getElementById("edit_buyer_name").value =
          this.dataset.buyerName || "";
        document.getElementById("edit_note").value = this.dataset.note || "";
      }

      showModal(editModal);
    });
  });

  // Update buttons
  const updateButtons = document.querySelectorAll(
    "#updateExpenseBtn, #updateSaleBtn"
  );
  updateButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const form = this.closest("form");
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const editModal = this.closest(".modal");
      const confirmModal = document.getElementById("confirmationModal");
      const confirmText = document.getElementById("confirmationText");
      confirmText.textContent = "Are you sure you want to update this?";
      confirmCallback = () => form.submit();
      hideModal(editModal);
      showModal(confirmModal);
    });
  });

  // Delete buttons
  document.querySelectorAll(".delete-expense-sale-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const deleteModal = document.querySelector(
        "#deleteExpenseModal, #deleteSaleModal"
      );

      // For Expense
      if (this.dataset.expenseId) {
        document.getElementById("deleteExpenseId").value =
          this.dataset.expenseId;
        document.getElementById("deleteExpenseCropName").textContent =
          this.dataset.cropName;
      }

      // For Sale
      if (this.dataset.saleId) {
        document.getElementById("deleteSaleId").value = this.dataset.saleId;
        document.getElementById("deleteSaleCropName").textContent =
          this.dataset.cropName;
      }

      showModal(deleteModal);
    });
  });

  // Cancel delete buttons
  document
    .querySelectorAll("#cancelDeleteExpenseBtn, #cancelDeleteSaleBtn")
    .forEach((btn) => {
      btn.addEventListener("click", function () {
        const modal = this.closest(".modal");
        hideModal(modal);
      });
    });

  // Delete All buttons
  document.querySelectorAll(".delete-all-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const deleteAllModal = document.getElementById("deleteAllModal");
      document.getElementById("deleteAllCropId").value = this.dataset.cropId;
      showModal(deleteAllModal);
    });
  });

  // Cancel Delete All
  document
    .getElementById("cancelDeleteAllBtn")
    .addEventListener("click", function () {
      hideModal(document.getElementById("deleteAllModal"));
    });

  // Confirmation modal buttons
  document.getElementById("confirmBtn").addEventListener("click", function () {
    if (confirmCallback) confirmCallback();
    hideModal(document.getElementById("confirmationModal"));
  });

  document.getElementById("cancelBtn").addEventListener("click", function () {
    hideModal(document.getElementById("confirmationModal"));
  });

  // Search
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      document.querySelectorAll(".crop-group").forEach((group) => {
        const cropName = group.dataset.cropName;
        if (cropName.includes(searchTerm)) {
          group.style.display = "block";
        } else {
          group.style.display = "none";
        }
      });
    });
  }

  // Close modal when clicking outside
  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("modal")) {
      hideModal(event.target);
    }
  });
});
