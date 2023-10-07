import { getBlogInfo } from './blog.js';


document.addEventListener("DOMContentLoaded", function() {
    // render blog name and title
    document.querySelector('.blog-footer-logo').textContent = getBlogInfo("blog_name");

    // the render ended, set back the scroll bar and hide the loading page

    // 0.3s delay to make animation smoother 
    setTimeout(function() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.querySelector('.loadingText');
        const innerBar = document.querySelector('.innerBar');
        
        loadingOverlay.style.opacity = '0';
        innerBar.style.opacity = '0'
        loadingText.style.opacity = '0'
        document.body.style.overflow = 'auto'

        loadingOverlay.addEventListener('transitionend', function() {
            loadingOverlay.style.display = 'none';
        });
    
    }, 300);
});
