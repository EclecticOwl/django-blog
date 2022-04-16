const messages = document.getElementById('messages')
const messageExit = document.getElementById('messageExit')

document.addEventListener("DOMContentLoaded", function(){
    if (messages) {
        messageExit.addEventListener('click', (e) => {
            messages.remove(messageExit)
        })
    }
    const menu_btn = document.querySelector('#hamburger');
    const mobile_menu = document.querySelector('#mobile-nav');

    menu_btn.addEventListener('click', function () {
	    menu_btn.classList.toggle('is-active');
	    mobile_menu.classList.toggle('is-active');
    });
});


   
