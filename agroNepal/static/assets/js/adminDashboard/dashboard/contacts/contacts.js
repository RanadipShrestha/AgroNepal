document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("deleteContactModal");
  const cancelBtn = document.getElementById("cancelDeleteContactBtn");
  const deleteBtns = document.querySelectorAll(".delete-contact-btn");
  const toast = document.getElementById("admin-message-toast");
  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      document.getElementById("deleteContactId").value =
        this.getAttribute("data-contactid");
      document.getElementById("deleteContactName").textContent =
        this.getAttribute("data-contactname");
      modal.classList.add("active");
    });
  });

  cancelBtn.addEventListener("click", function () {
    modal.classList.remove("active");
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.classList.remove("active");
    }
  });

  if (toast && toast.children.length > 0) {
    setTimeout(() => {
      const items = toast.getElementsByClassName("message-toast-item");
      for (let item of items) {
        item.style.animation = "fadeOut 0.5s ease-in forwards";
      }
      setTimeout(() => {
        toast.style.display = "none";
      }, 500);
    }, 4000);
  }
});
