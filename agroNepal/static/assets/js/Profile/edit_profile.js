function showConfirmation() {
  const form = document.getElementById("profileForm");

  if (form.checkVisibility()) {
    document.getElementById("confirmationOverlay").classList.add("active");
  } else {
    form.reportValidity();
  }
}

function closeConfirmation() {
  document.getElementById("confirmationOverlay").classList.remove("active");
}

function submitForm() {
  document.getElementById("profileForm").submit();
}

// Close modal when clicking outside of it
document.getElementById('confirmationOverlay').addEventListener('click', function(e) {
    if (e.target === this) {
        closeConfirmation();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeConfirmation();
    }
});