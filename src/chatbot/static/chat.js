const socket = io();

socket.on('message', function(msg) {
    addMessage('bot', msg);
});

function sendMessage() {
    let inputBox = document.getElementById('message-input');
    let message = inputBox.value;

    if (message.trim() !== '') {
        addMessage('user', message);
        socket.send(message);
        inputBox.value = '';
    }
}

function addMessage(sender, message) {
    let chatBox = document.getElementById('chat-box');
    let messageElement = document.createElement('div');
    messageElement.className = 'message ' + sender;

    let messageText = document.createElement('p');
    messageText.innerText = message;
    messageElement.appendChild(messageText);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
