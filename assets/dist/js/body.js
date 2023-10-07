import { getBlogInfo } from './blog.js';
import { getVisitorInfo } from './visitor.js';
import { fetchArticles } from './post.js';
import { displayMsgBox, Color } from './utils.js'
import { MSG_BOX_DISPLAY_TIME, MSG_BOX_ERRMSG_DISPLAY_TIME, LOADING_ERR_MSG, LOADING_TIMEOUT, NO_MORE_POST_MSG, INIT_RENDER_POST, RENDER_POST_PER_TIME } from './config.js'

document.addEventListener("DOMContentLoaded", function () {
    // render featured post
    const featuredPostContent = getBlogInfo('featured_post');
    document.getElementById('post-title').textContent = featuredPostContent.title;
    document.getElementById('post-content').textContent = featuredPostContent.leadContent;
    const postLinkElement = document.getElementById('post-link');
    postLinkElement.href = featuredPostContent.link;
    postLinkElement.textContent = "Continue reading...";

    // render visitor info
    const visitorInfo = getVisitorInfo();
    document.getElementById('userInfo').textContent = visitorInfo['name']

    // render three articles 
    document.querySelector('.skeleton-container-2').style.display = 'block';
    fetchArticles(0, INIT_RENDER_POST).then(newArticles => {
        newArticles.forEach(article => {
            renderArticle(article)
        });
        document.querySelector('.skeleton-container-2').style.display = 'none';
    })

    // render about
    document.getElementById('about-body').textContent = getBlogInfo("about")

    // render tag group
    const tags = getBlogInfo("tags");
    const tagGroup = document.getElementById('tag-group');
    
    tags.forEach(tag => {
        const cur_tag = document.createElement('button');
        cur_tag.setAttribute('type', 'button');
        cur_tag.className = 'btn btn-dark btn-sm tag mx-1';
        cur_tag.innerText = tag;
        
        tagGroup.appendChild(cur_tag);
    });  
});

function renderArticle(article) {
    const articleDiv = document.createElement('article');
    articleDiv.className = 'blog-post';

    const title = document.createElement('h2');
    title.className = 'blog-post-title';
    title.textContent = article.title;
    articleDiv.appendChild(title);

    const meta = document.createElement('p');
    meta.className = 'blog-post-meta';
    meta.innerHTML = `${article.meta.date}<span class="text-warning">&nbsp;&nbsp;${article.meta.word_count}</span>`;
    articleDiv.appendChild(meta);

    const content = document.createElement('p');
    content.textContent = article.description;
    articleDiv.appendChild(content);

    document.querySelector('.article_box').appendChild(articleDiv);
}

let canLoadMore = true;
let renderedPostsCount = INIT_RENDER_POST; 

function loadMoreContent() {
    if (!canLoadMore) {
        displayMsgBox(NO_MORE_POST_MSG, MSG_BOX_DISPLAY_TIME);
        return;
    };

    // Show the skeleton screen
    document.querySelector('.skeleton-container').style.display = 'block';

    const fetchPromise = fetchArticles(renderedPostsCount, renderedPostsCount + RENDER_POST_PER_TIME);
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error(LOADING_ERR_MSG)), LOADING_TIMEOUT);
    });

    Promise.race([fetchPromise, timeoutPromise])
        .then(newArticles => {
            // Once data is fetched, hide skeleton
            document.querySelector('.skeleton-container').style.display = 'none';

            // nothing to be loaded
            if (newArticles.length === 0) {
                canLoadMore = false;
                displayMsgBox(NO_MORE_POST_MSG, MSG_BOX_DISPLAY_TIME);
            } else {
                // Render the new articles
                newArticles.forEach(article => {
                    renderArticle(article);
                });

                renderedPostsCount += newArticles.length;
                canLoadMore = true;
            }
        })
        .catch(error => {
            document.querySelector('.skeleton-container').style.display = 'none';
            displayMsgBox(error.message, MSG_BOX_ERRMSG_DISPLAY_TIME, Color.RED);
        });
}


window.addEventListener('scroll', function () {
    // Check if user has scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadMoreContent();
    }
});

document.getElementById('subscribeForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission.

    const emailInput = document.querySelector('#email-address');

    if (emailInput.value && emailInput.validity.valid) {
        // TODO: subscribe email trigger
        console.log('Email is valid and ready to be submitted: ', emailInput.value);
    }
});

