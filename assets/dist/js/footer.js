import { getBlogInfo } from './blog.js';


document.addEventListener("DOMContentLoaded", function () {
    // render footer title
    document.querySelector('.blog-footer-logo').textContent = getBlogInfo("blog_name");

});
