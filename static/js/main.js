const messages = document.getElementById('messages')
const messageExit = document.getElementById('messageExit')
const userMessage = document.querySelectorAll('#profile_message_content')

if (messages) {
    messageExit.addEventListener('click', (e) => {
        messages.remove(messageExit)
    })
}
if (userMessage) {
    userMessage.forEach( message => {
        message.addEventListener('click', () => {
            window.location.href = message.dataset.href
        })
    })
}