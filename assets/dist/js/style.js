import { generateColor } from './tagColorPicker.js';


document.addEventListener('DOMContentLoaded', function () {
    // coloring tags
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        const color = generateColor(tag.textContent.trim());
        tag.style.backgroundColor = color;
    });
});


// ripple effect
document.querySelector('.article_box').addEventListener('click', function(event) {
    // Check if the clicked element or its parent is a .blog-post
    let blogPost = event.target.closest('.blog-post');

    if (!blogPost) return;  // If not, exit

    // Create span element for ripple
    let ripple = document.createElement('span');
    ripple.classList.add('ripple');

    // Compute size and position
    let rect = blogPost.getBoundingClientRect();
    let size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = event.clientX - rect.left - size/2 + 'px';
    ripple.style.top = event.clientY - rect.top - size/2 + 'px';

    // Append ripple to the article and remove after animation
    blogPost.appendChild(ripple);
    ripple.addEventListener('animationend', function() {
        ripple.remove();
    });
});
