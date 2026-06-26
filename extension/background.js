chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // Only trigger when the page is fully loaded and it's an HTTP/HTTPS URL
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
        
        // Send the URL to the Aegis backend
        fetch("http://127.0.0.1:5000/check_url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => res.json())
        .then(data => {
            // If the backend flags the site, inject the content script to show a warning
            if (data.label === "PHISHING" || data.label === "SUSPICIOUS") {
                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    files: ["content.js"]
                }, () => {
                    // Send the risk data to the injected script
                    chrome.tabs.sendMessage(tabId, {
                        action: "show_warning",
                        data: data
                    });
                });
            }
        })
        .catch(err => {
            console.error("Aegis background scan failed: ", err);
        });
    }
});
