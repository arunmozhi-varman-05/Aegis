document.addEventListener("DOMContentLoaded", () => {
  const strictnessSelect = document.getElementById("strictness");
  const statusDiv = document.getElementById("status");
  const whitelistUl = document.getElementById("whitelist");

  // Load saved strictness level
  chrome.storage.sync.get(["strictness"], (result) => {
    if (result.strictness) {
      strictnessSelect.value = result.strictness;
    }
  });

  // Save strictness level on change
  strictnessSelect.addEventListener("change", () => {
    const value = strictnessSelect.value;
    chrome.storage.sync.set({ strictness: value }, () => {
      statusDiv.style.display = "block";
      setTimeout(() => {
        statusDiv.style.display = "none";
      }, 2000);
    });
  });

  // Fetch whitelist from backend
  function loadWhitelist() {
    fetch("http://127.0.0.1:5000/whitelist")
      .then(res => res.json())
      .then(data => {
        whitelistUl.innerHTML = "";
        const domains = data.domains || [];
        
        if (domains.length === 0) {
          whitelistUl.innerHTML = "<li>No whitelisted domains yet.</li>";
          return;
        }

        domains.forEach(domain => {
          const li = document.createElement("li");
          li.textContent = domain;
          
          const btn = document.createElement("button");
          btn.textContent = "Remove";
          btn.className = "remove-btn";
          btn.onclick = () => removeDomain(domain);
          
          li.appendChild(btn);
          whitelistUl.appendChild(li);
        });
      })
      .catch(err => {
        whitelistUl.innerHTML = "<li>Error loading whitelist. Make sure API is running.</li>";
      });
  }

  // Remove domain from backend
  function removeDomain(domain) {
    fetch("http://127.0.0.1:5000/whitelist", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain: domain })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        loadWhitelist();
      }
    });
  }

  loadWhitelist();
});
