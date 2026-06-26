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
        backgroundColor: data.label.toUpperCase().includes("PHISHING") ? "#dc3545" : (data.label.toUpperCase().includes("SUSPICIOUS") ? "#ffc107" : "#28a745"),
        color: data.label.toUpperCase().includes("SUSPICIOUS") ? "black" : "white",
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

    let message = "";
    if (data.label.toUpperCase().includes("PHISHING")) {
        message = `⚠️ <b>Aegis Alert:</b> This website is flagged as <b>DANGEROUS/PHISHING</b> (Risk Score: ${data.risk_score}%). Proceed with extreme caution!`;
    } else if (data.label.toUpperCase().includes("SUSPICIOUS")) {
        message = `⚠️ <b>Aegis Alert:</b> This website is flagged as <b>SUSPICIOUS</b> (Risk Score: ${data.risk_score}%). Be careful.`;
    } else {
        message = `✅ <b>Aegis Alert:</b> This website is flagged as <b>LEGITIMATE</b> (Risk Score: ${data.risk_score}%). Safe browsing!`;
    }

    const textDiv = document.createElement("div");
    textDiv.innerHTML = message;
    
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
