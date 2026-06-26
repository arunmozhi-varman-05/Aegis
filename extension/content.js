function showBanner(data) {
    if (document.getElementById("aegis-warning-banner")) {
        return;
    }

    const banner = document.createElement("div");
    banner.id = "aegis-warning-banner";
    
    Object.assign(banner.style, {
        position: "fixed",
        top: "0",
        left: "0",
        width: "100%",
        backgroundColor: data.label.includes("PHISHING") ? "#dc3545" : "#ffc107",
        color: data.label.includes("PHISHING") ? "white" : "black",
        textAlign: "center",
        padding: "15px",
        zIndex: "999999",
        fontFamily: "Arial, sans-serif",
        fontSize: "16px",
        fontWeight: "bold",
        boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    });

    const textDiv = document.createElement("div");
    textDiv.innerHTML = `🛡️ <b>Aegis Alert:</b> This website is flagged as <b>${data.label}</b> (Risk Score: ${data.risk_score}%). Proceed with extreme caution!`;
    
    const closeBtn = document.createElement("button");
    closeBtn.innerText = "Dismiss";
    Object.assign(closeBtn.style, {
        backgroundColor: "white",
        color: "black",
        border: "none",
        padding: "5px 10px",
        cursor: "pointer",
        fontWeight: "bold",
        borderRadius: "3px",
        marginLeft: "20px"
    });

    closeBtn.onclick = () => banner.remove();

    banner.appendChild(textDiv);
    banner.appendChild(closeBtn);
    document.body.prepend(banner);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "show_warning") {
        showBanner(request.data);
    }
});

// ==========================================
// DOM Analysis (Client-side Security)
// ==========================================
function runDomAnalysis() {
    if (window.location.protocol === "http:") {
        const passwordField = document.querySelector('input[type="password"]');
        if (passwordField) {
            showBanner({
                label: "PHISHING (Unsecured Password)",
                risk_score: 100
            });
        }
    }
}

// Delay slightly to let the DOM settle
setTimeout(runDomAnalysis, 500);
