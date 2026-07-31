const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav_links');

hamburger.addEventListener('click', function(){
    navLinks.classList.toggle('nav_open');
});