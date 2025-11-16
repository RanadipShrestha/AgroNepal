const questions = document.querySelectorAll(".faq-question");

questions.forEach((question) => {
  question.addEventListener("click", () => {
    const answer = question.nextElementSibling;

    if (answer.classList.contains("active")) {
      answer.classList.remove("active");
      answer.style.maxHeight = null;
    }

    else {
      answer.classList.add("active");
      answer.style.maxHeight = answer.scrollHeight + "px";
    }
  });
});
