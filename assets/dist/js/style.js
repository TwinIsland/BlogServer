import { generateColor } from './tagColorPicker.js';


document.addEventListener('DOMContentLoaded', function () {
    // coloring tags
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        const color = generateColor(tag.textContent.trim());
        tag.style.backgroundColor = color;
    });
});

