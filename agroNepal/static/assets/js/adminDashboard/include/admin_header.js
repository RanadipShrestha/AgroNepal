// Profile dropdown toggle
const profileBtn = document.getElementById("admin-profile-btn");
const dropdownMenu = document.getElementById("dropdown-menu");

if (profileBtn && dropdownMenu) {
  profileBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdownMenu.classList.toggle("active");
  });

  document.addEventListener("click", function (e) {
    if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("active");
    }
  });
}

// Sidebar toggle for mobile
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".adminDashboard-menu-toggle");
  const sidebar = document.querySelector(".adminDashboardSidebar");

  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      sidebar.classList.toggle("active");
    });

    // Close sidebar when clicking outside
    document.addEventListener("click", (e) => {
      if (
        sidebar.classList.contains("active") &&
        !sidebar.contains(e.target) &&
        !menuToggle.contains(e.target)
      ) {
        sidebar.classList.remove("active");
      }
    });

    // Close sidebar when clicking on a link
    const sidebarLinks = sidebar.querySelectorAll("a");
    sidebarLinks.forEach((link) => {
      link.addEventListener("click", () => {
        sidebar.classList.remove("active");
      });
    });
  }
});
