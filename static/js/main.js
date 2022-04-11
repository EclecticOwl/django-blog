const messages = document.getElementById('messages')
const messageExit = document.getElementById('messageExit')

document.addEventListener("DOMContentLoaded", function(){
    if (messages) {
        messageExit.addEventListener('click', (e) => {
            messages.remove(messageExit)
        })
    }
});