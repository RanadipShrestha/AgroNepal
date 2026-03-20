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
