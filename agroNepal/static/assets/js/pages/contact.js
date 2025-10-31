document.querySelectorAll(".faq-question").forEach((q) => {
  q.addEventListener("click", () => {
    const answer = q.nextElementSibling;
    const isActive = answer.classList.toggle("active");
    answer.style.maxHeight = isActive ? `${answer.scrollHeight}px` : null;
  });
});
