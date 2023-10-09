document.addEventListener('DOMContentLoaded', function () {
    const tocList = document.getElementById('toc-list');
    const headers = document.querySelectorAll('.article-body h1, .article-body h2');

    headers.forEach((header, index) => {
        // Assign an ID to each header to link to
        const id = `header-${index + 1}`;
        header.id = id;

        // Create the TOC list item and link
        const listItem = document.createElement('li');
        const anchor = document.createElement('a');

        anchor.textContent = header.textContent;
        anchor.href = `#${id}`;
        anchor.classList.add('toc-link');

        // Indent h2 items for better visual hierarchy
        if (header.tagName === 'H2') {
            anchor.style.marginLeft = '20px';
        }

        listItem.appendChild(anchor);
        tocList.appendChild(listItem);
    });
});

// Function to highlight the active TOC entry
function highlightActiveTOCEntry() {
    const headers = document.querySelectorAll('.article-body h1, .article-body h2');
    let closestHeader = null;

    headers.forEach((header) => {
        const rect = header.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.3 && rect.bottom > 0) {
            closestHeader = header;
        }
    });

    if (closestHeader) {
        const tocLinks = document.querySelectorAll('.toc-link');
        tocLinks.forEach((link) => link.classList.remove('active'));

        const activeLink = document.querySelector(`.toc-link[href="#${closestHeader.id}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
}

// Listen for the scroll event
window.addEventListener('scroll', highlightActiveTOCEntry);
