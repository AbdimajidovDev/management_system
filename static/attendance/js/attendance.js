document.addEventListener("DOMContentLoaded", function () {
  const toggles = document.querySelectorAll(".status-toggle");

  toggles.forEach(toggle => {
    if (toggle.hasAttribute('data-disabled')) return;

    const input = toggle.querySelector("input");
    const statusSpan = toggle.querySelector(".status");
    const statuses = ["p", "a", "e"];
    const classes = {
      "e": "status-e", // 🔳
      "p": "status-p", // ✅
      "a": "status-a"  // ❌
    };

    let parts = input.value.split("_");
    if (parts.length < 3) {
      input.value = `${toggle.dataset.student}_${toggle.dataset.date}_e`;
      parts = input.value.split("_");
    }

    toggle.addEventListener("click", () => {
      const current = parts[2];
      const currentIndex = statuses.indexOf(current);
      const nextIndex = (currentIndex + 1) % statuses.length;
      const nextStatus = statuses[nextIndex];

      input.value = `${toggle.dataset.student}_${toggle.dataset.date}_${nextStatus}`;
      parts[2] = nextStatus;
      statusSpan.className = `status ${classes[nextStatus]}`;
    });
  });
});
