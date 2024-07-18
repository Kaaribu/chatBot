document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed')
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

function sendMessage() {
    var userInput = document.getElementById("user-input").value.trim();
    console.log('User Input', userInput.value);
    if (!userInput) {
        return;
    }

    const chatBox = document.getElementById("chat-box");

    // User message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = `User: ${userInput}`;
    chatBox.appendChild(userMessage);

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send user message to Flask backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, user_id: 'user123' })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server Response: ', data);  // Debugging statement
        // Bot response
        const botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}