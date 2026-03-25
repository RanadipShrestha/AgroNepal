function openEditModal(id, name, desc) {
  document.getElementById("edit_crop_id").value = id;
  document.getElementById("edit_crop_name").value = name;
  document.getElementById("edit_crop_desc").value = desc === "None" ? "" : desc;

  const container = document.getElementById("editSchedulesContainer");
  if (container) container.innerHTML = "";

  const schedulesData = document.getElementById(`schedules-json-${id}`);
  if (schedulesData) {
    try {
      const schedules = JSON.parse(schedulesData.textContent);
      schedules.forEach((schedule) => {
        addScheduleRow("edit", schedule.day_number, schedule.task);
      });
    } catch (e) {
      console.error("Could not parse schedules JSON");
    }
  }

  document.getElementById("editModal").style.display = "flex";
}

function addScheduleRow(mode, dayValue = "", taskValue = "") {
  const containerId =
    mode === "add" ? "addSchedulesContainer" : "editSchedulesContainer";
  const container = document.getElementById(containerId);

  if (!container) return;

  const row = document.createElement("div");
  row.style.display = "flex";
  row.style.gap = "0.5rem";
  row.style.alignItems = "center";

  // Prevent JS injection issues
  const safeDay = String(dayValue).replace(/"/g, "&quot;");
  const safeTask = String(taskValue).replace(/"/g, "&quot;");

  row.innerHTML = `
        <input type="number" name="schedule_day[]" class="form-input" style="width: 80px; margin-bottom: 0;" placeholder="Day" value="${safeDay}" min="0" required>
        <input type="text" name="schedule_task[]" class="form-input" style="flex: 1; margin-bottom: 0;" placeholder="Task (e.g. Watering)" value="${safeTask}" required>
        <button type="button" onclick="this.parentElement.remove()" style="background: none; border: none; color: #ef4444; cursor: pointer; padding: 4px;">
            <i class="fa-solid fa-trash"></i>
        </button>
    `;

  container.appendChild(row);
}

// Custom Delete Modal Logic
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("cropSearchInput");
  if (searchInput) {
    searchInput.addEventListener("keyup", function () {
      const filter = searchInput.value.toLowerCase();
      const rows = document.querySelectorAll(".admin-table tbody tr");

      rows.forEach((row) => {
        if (row.children.length === 1) return; // skip "No crops defined" placeholder
        const text = row.textContent.toLowerCase();
        if (text.includes(filter)) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });
    });
  }

  const deleteModal = document.getElementById("deleteCropModal");
  const cancelDeleteBtn = document.getElementById("cancelDeleteCropBtn");
  const deleteBtns = document.querySelectorAll(".delete-crop-btn");

  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      document.getElementById("deleteCropId").value =
        this.getAttribute("data-cropid");
      document.getElementById("deleteCropName").textContent =
        this.getAttribute("data-cropname");
      deleteModal.classList.add("active");
    });
  });

  cancelDeleteBtn.addEventListener("click", function () {
    deleteModal.classList.remove("active");
  });

  // Add Confirmation Logic
  const confirmAddModal = document.getElementById("confirmAddModal");
  const confirmEditModal = document.getElementById("confirmEditModal");

  document
    .getElementById("triggerAddConfirmBtn")
    .addEventListener("click", function () {
      const form = document.getElementById("addCropForm");
      if (form.checkValidity()) {
        confirmAddModal.classList.add("active");
      } else {
        form.reportValidity();
      }
    });

  document
    .getElementById("cancelAddBtn")
    .addEventListener("click", function () {
      confirmAddModal.classList.remove("active");
    });

  document
    .getElementById("confirmAddBtn")
    .addEventListener("click", function () {
      document.getElementById("addCropForm").submit();
    });

  // Edit Confirmation Logic
  document
    .getElementById("triggerEditConfirmBtn")
    .addEventListener("click", function () {
      const form = document.getElementById("editCropForm");
      if (form.checkValidity()) {
        confirmEditModal.classList.add("active");
      } else {
        form.reportValidity();
      }
    });

  document
    .getElementById("cancelEditBtn")
    .addEventListener("click", function () {
      confirmEditModal.classList.remove("active");
    });

  document
    .getElementById("confirmEditBtn")
    .addEventListener("click", function () {
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
