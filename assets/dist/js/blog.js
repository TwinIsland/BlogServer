export function getBlogInfo(key = null) {
    // Sample data for demonstration purposes
    let blogInfo = JSON.parse(sessionStorage.getItem('blogInfo'));

    if (!blogInfo) {
        blogInfo = {
            blog_name: "贰岛",
            blog_title: "贰岛博客",
            about: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit dolorem, reprehenderit quisquam esse nam facere sunt ipsam soluta accusantium incidunt, neque molestias necessitatibus non laborum unde rem ea voluptates minima!",
            tags: ["Technology", "AI", "Programming", "Web Development", "Philosophy", "Education", "Research", "Innovation", "Design", "Tutorials"],

            featured_post: {
                title: "CS361: 期中 Review",
                leadContent: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus sunt qui reprehenderit nihil possimus molestias iusto illo fugiat, excepturi aspernatur quo unde nulla libero maxime soluta eaque debitis voluptatem itaque.",
                link: "./post.html"
            },

            trend_post: [
                {
                    title: "CS361: 期中 Review",
                    leadContent: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus sunt qui reprehenderit nihil possimus molestias iusto illo fugiat, excepturi aspernatur quo unde nulla libero maxime soluta eaque debitis voluptatem itaque.",
                    link: "./post.html"
                },    
                {
                    title: "CS361: 期中 Review",
                    leadContent: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus sunt qui reprehenderit nihil possimus molestias iusto illo fugiat, excepturi aspernatur quo unde nulla libero maxime soluta eaque debitis voluptatem itaque.",
                    link: "./post.html"
                }
            ],

            archives: [
                { k: "January 2021", link: "./jan2021" },
                { k: "February 2021", link: "./feb2021" },
                { k: "March 2021", link: "./mar2021" },
                { k: "April 2021", link: "./apr2021" },
                { k: "May 2021", link: "./may2021" },
                { k: "June 2021", link: "./jun2021" },
                { k: "July 2021", link: "./jul2021" },
                { k: "August 2021", link: "./aug2021" },
                { k: "September 2021", link: "./sep2021" }
            ],

            navLinks: [
                { text: "首页", href: "#" },
                { text: "笔记", href: "#" },
                { text: "追番", href: "#" },
                { text: "关于", href: "#" },
                { text: "相册", href: "#" },
                { text: "存档", href: "#" },
                { text: "友链", href: "#" },
                { text: "实验室", href: "#" },
            ],

            about: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit dolorem, reprehenderit quisquam esse nam facere sunt ipsam soluta accusantium incidunt, neque molestias necessitatibus non laborum unde rem ea voluptates minima!"
        };

        // set local storage is first initialized
        sessionStorage.setItem('blogInfo', JSON.stringify(blogInfo));
    }
    if (key == null) return blogInfo;
    return blogInfo[key];
}

