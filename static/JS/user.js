const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav_links');

if (hamburger && navLinks) {
hamburger.addEventListener('click', function(){
    navLinks.classList.toggle('nav_open');
  });
}

// On clicking a thumbnail it becomes the cover image

const productImg = document.querySelector('.product_cover img');
const thumbnails = document.querySelectorAll('.thumbnail');

if (productImg && thumbnails) {
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function(){
            productImg.src = thumbnail.querySelector('img').src
            thumbnails.forEach(thumbnail => {
                thumbnail.classList.remove('active'); 
            });
            thumbnail.classList.add('active');
        });
    });
}

// Massage us Button in contact page copies the name and message,
// to the whatsapp message box
const textButton = document.querySelector('#textButton');
if (textButton) {
    textButton.addEventListener('click', function(){
        const name = document.querySelector('#name').value;
        const message = document.querySelector('#message').value;
        const fullmessage = `Hello, my name is ${name}. ${message}`;
        const url = `https://wa.me/254768274141?text=${encodeURIComponent(fullmessage)}`;
        window.location.href = url;
    });
}