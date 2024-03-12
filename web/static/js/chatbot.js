function sendMessage(addMessageToList = true, messageContent = null, messageSender = 'user') {
    // Get the input field value
    messageContent ||= document.querySelector('.chat-input').value.trim();

    // If input field is empty, do nothing
    if (messageContent === '') {
        return;
    }

    // Clear the input field after sending the message
    document.querySelector('.chat-input').value = '';

    // Construct the message object
    const message = {
        sender: messageSender,
        content: messageContent
    };

    // Add the message to the chat messages list
    if (addMessageToList) {
        addMessage(message)
        addMessage({ sender: 'assistant pending', content: '...'})
    }

    // Make a POST request to the '/messages' endpoint
    fetch('/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(message)
    })
        .then(response => response.json())
        .then(data => {
            // The response includes all messages, so we need to clear the
            // history before adding each message to the chat messages list.
            const chatMessages = document.querySelector('.chat-messages');
            chatMessages.innerHTML = '';
            data.forEach(function(message) {
                addMessage(message)
            ;});
        })
        .catch(error => {
            console.error('Error sending message:', error);
            // return the message to the text input so the user can try again
            // or copy the message to the clipboard (losing input sucks!)
            document.querySelector('.chat-input').value = messageContent
        })
        .finally(() => {
            chatInput.disabled = false
            chatInput.focus()
        });
}

function addMessage(message) {
    // Create a new list item for the message
    const messageElement = document.createElement('li');
    messageElement.classList.add('message', ...message.sender.split(' '));
    messageElement.textContent = message.content;

    // Append the new message to the chat messages list
    const chatMessages = document.querySelector('.chat-messages');
    chatMessages.appendChild(messageElement);

    // Scroll the chat window to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateCourseMaterials(courseContent) {
    fetch('/course_materials', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(courseContent)
    })
        .then(response => response.json())
        .then(data => {
            // The response includes all messages, so we need to clear the
            // history and then add each message to the chat messages list.
            const chatMessages = document.querySelector('.chat-messages');
            chatMessages.innerHTML = '';
            data.forEach(function(message) {
                addMessage(message)
            ;});
            
            // We are ready to go, enable the text input field!
            chatInput.placeholder = 'Type a message...'
            chatInput.disabled = false
            chatInput.focus()
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
}

function postMessageGetPageContent() {
    const canvas_domain_origin = 'http://canvas-web.inseng.test/'
    window.parent.postMessage({ subject: 'getPageContent' }, canvas_domain_origin)
}

function initializePage() {
    chatInput = document.getElementById('messageInput')

    // Add event listener for message input field
    chatInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            chatInput.disabled = true;
            sendMessage();
        }
    });

    // Add event listener for postMessage from Canvas
    window.addEventListener('message', (event) => {
        console.log('Received message from Canvas:', event)
        // TODO get parent origin from launch parameters
        if (event.origin !== 'http://canvas-web.inseng.test') return

        if (event.data.subject === 'canvasPageContent') {
            console.log('Canvas page content:', event.data.content)
            updateCourseMaterials(event.data.content)
        }
    })
    // Request the page content from Canvas
    postMessageGetPageContent()
}

initializePage()