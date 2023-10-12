import { getBlogInfo } from './blog.js';
import { OVERLAY_LOADING_TEXT } from './config.js'
import { getVisitorInfo } from './visitor.js';


document.addEventListener("DOMContentLoaded", function() {
    // render blog name and title
    document.title = getBlogInfo("blog_title");

    document.querySelector('.blog-header-logo').textContent = getBlogInfo("blog_name");

    // render navLinks
    const navLinks = getBlogInfo("navLinks");
    const navElement = document.getElementById('navContainer');

    navLinks.forEach(link => {
        const aTag = document.createElement('a');
        aTag.className = 'p-2 link-secondary';
        aTag.href = link.link;
        aTag.textContent = link.text;
        navElement.appendChild(aTag);
    });

    // render visitor info
    const visitorInfo = getVisitorInfo();
    document.getElementById('userInfo').textContent = visitorInfo['name']
    
});

// search
document.getElementById('tag-input').addEventListener('keyup', function (event) {
    // Check if the Enter key was pressed
    if (event.key === 'Enter' && this.value.trim() !== "" && this.value.trim().startsWith('#')) {
        const tagList = document.querySelector('.tag-list');

        // Create the tag element
        const tagElem = document.createElement('span');
        tagElem.className = 'badge bg-secondary me-2';
        tagElem.textContent = this.value.trim().slice(1);

        // Add a close button to the tag
        const closeButton = document.createElement('button');
        closeButton.className = 'btn-close ms-2';
        closeButton.type = 'button';
        closeButton.addEventListener('click', function () {
            tagList.removeChild(tagElem);
        });
        tagElem.appendChild(closeButton);

        // Append the tag to the tag list
        tagList.appendChild(tagElem);

        // Clear the input
        this.value = "";
    } else if (event.key === 'Enter') {
        // Start search
        const tagList = document.querySelector('.tag-list');
        let query = {
            "tags": [],
            "query": this.value
        }
        while (tagList.firstChild) {
            query.tags.push(tagList.firstChild.textContent.trim());
            tagList.removeChild(tagList.firstChild);
        }

        this.value = "";
        console.log(query);
    }
});