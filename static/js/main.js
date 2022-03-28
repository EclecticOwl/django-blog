
const messages = document.getElementById('messages')

const messageExit = document.getElementById('messageExit')


messageExit.addEventListener('click', (e) => {
    messages.remove(messageExit)
})