document.querySelectorAll(".view-event-trigger").forEach(function (btn) {
  btn.addEventListener("click", function () {
    const img = document.getElementById("view-modal-img");
    const icon = document.getElementById("view-modal-icon");
    if (this.dataset.image) {
      img.src = this.dataset.image;
      img.style.display = "block";
      icon.style.display = "none";
    } else {
      img.style.display = "none";
      icon.style.display = "inline";
    }
    document.getElementById("view-modal-name").textContent = this.dataset.name;
    document.getElementById("view-modal-price").textContent =
      "Rs. " + this.dataset.price;
    document.getElementById("view-modal-tickets").textContent =
      this.dataset.available + " / " + this.dataset.total + " tickets";
    document.getElementById("view-modal-guest").textContent =
      this.dataset.guest;
    document.getElementById("view-modal-location").textContent =
      this.dataset.location;
    document.getElementById("view-modal-date").textContent = this.dataset.date;
    document.getElementById("view-modal-time").textContent =
      this.dataset.start + " (" + this.dataset.duration + ")";
    document.getElementById("view-modal-description").textContent =
      this.dataset.description;
    document.getElementById("eventViewModal").classList.add("active");
  });
});

const deleteModal = document.getElementById("deleteEventModal");
const deleteEventName = document.getElementById("deleteEventName");
const deleteEventId = document.getElementById("deleteEventId");

document.querySelectorAll(".delete-event-trigger").forEach((btn) => {
  btn.addEventListener("click", () => {
    deleteEventName.textContent = btn.dataset.name;
    deleteEventId.value = btn.dataset.id;
    deleteModal.classList.add("active");
  });
});

function closeDeleteModal() {
  deleteModal.classList.remove("active");
}

window.onclick = function (event) {
  if (event.target == deleteModal) {
    closeDeleteModal();
  }
};