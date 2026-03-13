const body = document.getElementById("popupBody");
const resultDiv = document.getElementById("result");
const checkBtn = document.getElementById("checkBtn");

// 🔁 Common scan function
function scanCurrentTab() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0].url;

    fetch("http://127.0.0.1:5000/check_url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    })
      .then(res => res.json())
      .then(data => {

        // Reset
        body.style.color = "#000";

        // 🎨 Color-coded background
        if (data.label === "LEGITIMATE") {
          body.style.backgroundColor = "#d4edda"; // green
        } 
        else if (data.label === "SUSPICIOUS") {
          body.style.backgroundColor = "#fff3cd"; // yellow
        } 
        else {
          body.style.backgroundColor = "#f8d7da"; // red
        }

        resultDiv.innerHTML = `
          🔎 <b>Domain:</b> ${data.domain}<br>
          📊 <b>Risk:</b> ${data.risk_score}%<br>
          🚦 <b>Status:</b> ${data.label}
        `;
      })
      .catch(() => {
        body.style.backgroundColor = "#f8d7da";
        resultDiv.innerText = "❌ Backend not running";
      });
  });
}

// 🚀 AUTO-SCAN when popup opens
document.addEventListener("DOMContentLoaded", scanCurrentTab);

// 🔘 Manual re-scan button
checkBtn.addEventListener("click", scanCurrentTab);

document.getElementById("markSafeBtn").addEventListener("click", () => {
  fetch("http://127.0.0.1:5000/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      domain: currentDomain,
      action: "mark_safe"
    })
  })
  .then(res => res.json())
  .then(data => {
    alert("Domain marked as trusted!");
  });
});

