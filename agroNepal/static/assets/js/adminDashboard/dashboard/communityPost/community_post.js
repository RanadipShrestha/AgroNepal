document.addEventListener("DOMContentLoaded", function () {
  const confirmModal = document.getElementById("confirmModal");
  const postForm = document.getElementById("postForm");

  const triggerConfirmBtn = document.getElementById(
    "communityPostTriggerConfirmBtn",
  );
  if (triggerConfirmBtn) {
    triggerConfirmBtn.addEventListener("click", function () {
      if (postForm.checkValidity()) {
        confirmModal.classList.add("active");
      } else {
        postForm.reportValidity();
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
      postForm.submit();
    });
  }

  window.addEventListener("click", function (event) {
    if (event.target === confirmModal) {
      confirmModal.classList.remove("active");
    }
  });
});


document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("deletePostModal");
    const cancelBtn = document.getElementById("cancelDeletePostBtn");
    const deleteBtns = document.querySelectorAll(".delete-post-btn");
    
    deleteBtns.forEach(btn => {
        btn.addEventListener("click", function() {
            document.getElementById("deletePostId").value = this.getAttribute("data-postid");
            document.getElementById("deletePostTitle").textContent = this.getAttribute("data-posttitle");
            modal.classList.add("active");
        });
    });
    
    cancelBtn.addEventListener("click", function() {
        modal.classList.remove("active");
    });
    
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.classList.remove("active");
        }
    });
});