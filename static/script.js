function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (message === "") return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div><b>You:</b> ${message}</div>`;

    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<div><b>Bot:</b> ${data.response}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    input.value = "";
    input.focus();
}
