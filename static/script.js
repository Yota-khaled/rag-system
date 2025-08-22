// Send message when clicking the button
document.getElementById("send-btn").addEventListener("click", sendMessage);

// Send message when pressing Enter
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        addMessage("bot", data.reply);
    });
}

function addMessage(sender, text) {
    let chatBox = document.getElementById("chat-box");
    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    if (sender === "bot") {
        let avatar = document.createElement("img");
        avatar.src = "/static/bot.png";
        avatar.classList.add("avatar");
        msgDiv.appendChild(avatar);
    }

    let bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;

    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle PDF upload
document.getElementById("pdf-upload").addEventListener("change", function() {
    let file = this.files[0];
    if (!file) return;

    let chatBox = document.getElementById("chat-box");
    let processingMsg = document.createElement("div");
    processingMsg.classList.add("message", "bot");
    processingMsg.innerHTML = `<img src="/static/bot.png" class="avatar"><div class="bubble"><em>Processing the PDF...</em></div>`;
    chatBox.appendChild(processingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    let formData = new FormData();
    formData.append("pdf", file);

    fetch("/upload_pdf", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        processingMsg.querySelector(".bubble").innerHTML = `<strong>${data.message}</strong>`;
    })
    .catch(() => {
        processingMsg.querySelector(".bubble").innerHTML = `<strong style="color:red;">An error occurred while processing the PDF</strong>`;
    });
});
