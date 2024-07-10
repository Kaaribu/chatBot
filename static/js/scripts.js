function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") {
        return;
    }

    var chatBox = document.getElementById("chat-box");
    var userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    document.getElementById("user-input").value = "";

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, user_id: 'user123' })
    })
    .then(response => response.json())
    .then(data => {
        var botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
