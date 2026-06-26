chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "show_warning") {
        const data = request.data;
        
        // Check if banner already exists to prevent duplicates
        if (document.getElementById("aegis-warning-banner")) {
            return;
        }

        const banner = document.createElement("div");
        banner.id = "aegis-warning-banner";
        
        // Styling the banner
        Object.assign(banner.style, {
            position: "fixed",
            top: "0",
            left: "0",
            width: "100%",
            backgroundColor: data.label === "PHISHING" ? "#dc3545" : "#ffc107",
            color: data.label === "PHISHING" ? "white" : "black",
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

        closeBtn.onclick = () => {
            banner.remove();
        };

        banner.appendChild(textDiv);
        banner.appendChild(closeBtn);
        document.body.prepend(banner);
    }
});
