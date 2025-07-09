// static/attendance/js/attendance.js

document.addEventListener("DOMContentLoaded", function () {
  const toggles = document.querySelectorAll(".status-toggle");

  toggles.forEach(toggle => {
    if (toggle.hasAttribute('data-disabled')) return; // o'qituvchilar uchun faqat bugungi sana

    const input = toggle.querySelector("input");
    const statusSpan = toggle.querySelector(".status");
    const statuses = ["e", "p", "a"]; // empty, present, absent
    const classes = {
      "e": "status-e",
      "p": "status-p",
      "a": "status-a"
    };

    toggle.addEventListener("click", () => {
      const current = input.value.split("_")[2];
      const nextIndex = (statuses.indexOf(current) + 1) % statuses.length;
      const nextStatus = statuses[nextIndex];

      input.value = `${toggle.dataset.student}_${toggle.dataset.date}_${nextStatus}`;
      statusSpan.className = `status ${classes[nextStatus]}`;
    });
  });
});
