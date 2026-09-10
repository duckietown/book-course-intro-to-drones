/* Book-local practice questions. No storage, network requests, or score tracking. */
(() => {
  "use strict";
  function enhance() {
    document.querySelectorAll("fieldset.dt-question").forEach((question) => {
      if (question.dataset.enhanced) return;
      const radios = [...question.querySelectorAll('input[type="radio"]')];
      const button = question.querySelector(".dt-question-check");
      const status = question.querySelector(".dt-question-status");
      const solution = question.querySelector(".dt-question-solution");
      if (!radios.length || !button || !status || !solution) return;

      button.addEventListener("click", () => {
        const selected = radios.find((radio) => radio.checked);
        if (!selected) {
          status.textContent = "Choose an answer before checking.";
          radios[0].focus();
          return;
        }
        const correct = selected.value === solution.dataset.answer;
        status.textContent = (correct ? "Correct. " : "Incorrect. ") +
          (correct ? solution.dataset.feedbackCorrect : solution.dataset.feedbackIncorrect);
        status.dataset.result = correct ? "correct" : "incorrect";
      });
      radios.forEach((radio) => {
        radio.addEventListener("change", () => {
          status.textContent = "";
          delete status.dataset.result;
        });
        // Clear browser-restored selections: each page load starts a fresh attempt.
        radio.checked = false;
        radio.disabled = false;
      });
      solution.hidden = true;
      button.hidden = false;
      question.dataset.enhanced = "true";
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhance, { once: true });
  } else {
    enhance();
  }
})();
