import {
    SOCIAL_MEDIA_BILIBILI, SOCIAL_MEDIA_GITHUB, SOCIAL_MEDIA_EMAIL_TRIM
} from './config.js'

document.addEventListener("DOMContentLoaded", function () {

    // render social medias
    document.getElementById("github-link").href = SOCIAL_MEDIA_GITHUB
    document.getElementById("email-p1").textContent = SOCIAL_MEDIA_EMAIL_TRIM.split(' ')[0]
    document.getElementById("email-p2").textContent = SOCIAL_MEDIA_EMAIL_TRIM.split(' ')[1]
    document.getElementById("email-p3").textContent = SOCIAL_MEDIA_EMAIL_TRIM.split(' ')[2]
    document.getElementById("bilibili-link").href = SOCIAL_MEDIA_BILIBILI
});
