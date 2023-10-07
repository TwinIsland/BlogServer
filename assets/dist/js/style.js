import { generateColor } from './tagColorPicker.js';


document.addEventListener('DOMContentLoaded', function () {
    // add click effect on every post 
    let blogPosts = document.querySelectorAll('.blog-post');

    blogPosts.forEach(function (blogPost) {
        blogPost.addEventListener('click', function (event) {
            let ripple = document.createElement("span");
            ripple.classList.add('ripple');
            let size = Math.max(this.offsetWidth, this.offsetHeight);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${event.pageX - this.offsetLeft - size / 2}px`;
            ripple.style.top = `${event.pageY - this.offsetTop - size / 2}px`;
            this.appendChild(ripple);
            ripple.addEventListener('animationend', function () {
                ripple.remove();
            });
        });
    });

    // coloring tags
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        const color = generateColor(tag.textContent.trim());
        tag.style.backgroundColor = color;
    });
});
