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
            // Read strictness level (not strictly needed now since we always show a banner, but kept for future use)
            chrome.storage.sync.get(["strictness"], (result) => {
                // Always show the classification banner on any website as requested
                chrome.tabs.sendMessage(tabId, {
                    action: "show_warning",
                    data: data
                });
            });
        })
        .catch(err => {
            console.error("Aegis background scan failed: ", err);
        });
    }
});
