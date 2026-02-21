document.addEventListener("DOMContentLoaded", function () {
  // Add Share Modal
  const addShareBtn = document.getElementById("addShareBtn");
  const addShareModal = document.getElementById("addShareModal");
  const closeShareModalBtn = document.getElementById("closeShareModalBtn");
  const addShareForm = document.getElementById("addShareForm");

  // Confirm Share Modal
  const confirmShareModal = document.getElementById("confirmShareModal");
  const confirmPublishShareBtn = document.getElementById(
    "confirmPublishShareBtn",
  );
  const cancelPublishShareBtn = document.getElementById(
    "cancelPublishShareBtn",
  );

  if (addShareBtn) {
    addShareBtn.addEventListener("click", function () {
      addShareModal.style.display = "block";
    });
  }

  if (closeShareModalBtn) {
    closeShareModalBtn.addEventListener("click", function () {
      addShareModal.style.display = "none";
    });
  }

  if (addShareForm) {
    addShareForm.addEventListener("submit", function (e) {
      e.preventDefault();
      addShareModal.style.display = "none";
      confirmShareModal.style.display = "block";
    });
  }

  if (confirmPublishShareBtn) {
    confirmPublishShareBtn.addEventListener("click", function () {
      confirmShareModal.style.display = "none";
      addShareForm.submit();
    });
  }

  if (cancelPublishShareBtn) {
    cancelPublishShareBtn.addEventListener("click", function () {
      confirmShareModal.style.display = "none";
      addShareModal.style.display = "block";
    });
  }

  // Edit Share Modal
  const editShareModal = document.getElementById("editShareModal");
  const closeEditShareModalBtn = document.getElementById(
    "closeEditShareModalBtn",
  );
  const editShareBtns = document.querySelectorAll(".edit-share-btn");

  editShareBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const shareId = this.getAttribute("data-share-id");
      const title = this.getAttribute("data-share-title");
      const description = this.getAttribute("data-share-description");
      const content = this.getAttribute("data-share-content");

      document.getElementById("editShareId").value = shareId;
      document.getElementById("edit_title").value = title;
      document.getElementById("edit_description").value = description;
      document.getElementById("edit_content").value = content;

      editShareModal.style.display = "block";
    });
  });

  if (closeEditShareModalBtn) {
    closeEditShareModalBtn.addEventListener("click", function () {
      editShareModal.style.display = "none";
    });
  }

  // Confirm Edit Share Logic
  const confirmEditShareModal = document.getElementById(
    "confirmEditShareModal",
  );
  const confirmEditShareUpdateBtn = document.getElementById(
    "confirmEditShareUpdateBtn",
  );
  const cancelEditShareUpdateBtn = document.getElementById(
    "cancelEditShareUpdateBtn",
  );
  const editShareForm = document.getElementById("editShareForm");

  if (editShareForm) {
    editShareForm.addEventListener("submit", function (e) {
      e.preventDefault();
      editShareModal.style.display = "none";
      confirmEditShareModal.style.display = "block";
    });
  }

  if (confirmEditShareUpdateBtn) {
    confirmEditShareUpdateBtn.addEventListener("click", function () {
      confirmEditShareModal.style.display = "none";
      editShareForm.submit();
    });
  }

  if (cancelEditShareUpdateBtn) {
    cancelEditShareUpdateBtn.addEventListener("click", function () {
      confirmEditShareModal.style.display = "none";
      editShareModal.style.display = "block";
    });
  }

  // Delete Share Modal
  const deleteShareModal = document.getElementById("deleteShareModal");
  const cancelDeleteShareBtn = document.getElementById("cancelDeleteShareBtn");
  const deleteShareBtns = document.querySelectorAll(".delete-share-btn");

  deleteShareBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const shareId = this.getAttribute("data-share-id");
      const shareTitle = this.getAttribute("data-share-title");

      document.getElementById("deleteShareId").value = shareId;
      document.getElementById("deleteShareTitle").textContent = shareTitle;

      deleteShareModal.style.display = "block";
    });
  });

  if (cancelDeleteShareBtn) {
    cancelDeleteShareBtn.addEventListener("click", function () {
      deleteShareModal.style.display = "none";
    });
  }

  // Close modals when clicking outside
  window.addEventListener("click", function (event) {
    if (event.target === addShareModal) {
      addShareModal.style.display = "none";
    }
    if (event.target === editShareModal) {
      editShareModal.style.display = "none";
    }
    if (event.target === deleteShareModal) {
      deleteShareModal.style.display = "none";
    }
    if (event.target === confirmShareModal) {
      confirmShareModal.style.display = "none";
      addShareModal.style.display = "block";
    }
    if (event.target === confirmEditShareModal) {
      confirmEditShareModal.style.display = "none";
      editShareModal.style.display = "block";
    }
  });

  // Search functionality
  const searchInput = document.getElementById("shareSearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const shareCards = document.querySelectorAll(".shareKnowledge-card");

      shareCards.forEach((card) => {
        const shareTitle = card.getAttribute("data-share-title");
        if (shareTitle.includes(searchTerm)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  }

  // Auto-hide alerts after 5s
  setTimeout(() => {
    const alerts = document.querySelectorAll(".shareKnowledge-alert");
    alerts.forEach((alert) => {
      alert.style.opacity = "0";
      alert.style.transform = "translateX(20px)";
      alert.style.transition = "all 0.5s ease";
      setTimeout(() => alert.remove(), 500);
    });
  }, 5000);
});
