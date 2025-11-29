let currentForm = null;

setTimeout(function () {
  const messages = document.querySelector(".messages");
  if (messages) {
    messages.style.transition = "opacity 0.5s, transform 0.5s";
    messages.style.transform = "translateX(100%)";
    setTimeout(() => messages.remove(), 500);
  }
}, 3000);


document.querySelectorAll(".delete-btn-trigger").forEach((button) => {
  button.addEventListener("click", () => {
    currentForm = button.closest("form");
    document.getElementById("deleteModal").style.display = "block";
    document.body.style.overflow = "hidden";
  });
});


function closeModal() {
  document.getElementById("deleteModal").style.display = "none";
  document.body.style.overflow = "auto";
  currentForm = null;
}

function confirmDelete() {
  if (currentForm) {
    currentForm.submit();
  }
}

window.onclick = function (event) {
  const modal = document.getElementById("deleteModal");
  if (event.target === modal) {
    closeModal();
  }
};

