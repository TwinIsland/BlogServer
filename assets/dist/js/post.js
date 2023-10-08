function request_article(from, to) {
    // Sample data for demonstration purposes

    const PostMetas = [
        {
            title: "CS412: Note for Midterm1",
            meta: {
                date: "APR 05, 2023",
                word_count: "662 Words",
                cover_img: "https://api.erdao.me/anipic?v=1"
            },
            description: "Lorem ipsum aasdad",
        },
        {
            title: "CS412: Lecture 2",
            meta: {
                date: "APR 05, 2023",
                word_count: "662 Words",
                cover_img: "https://api.erdao.me/anipic?v=2"
            },
            description: "Lorem ipsum aasdad",
        },
        {
            title: "Finger - 贝斯点弦练习",
            meta: {
                date: "APR 05, 2023",
                word_count: "662 Words",
                cover_img: "https://api.erdao.me/anipic?v=3"
            },
            description: "Lorem ipsum aasdad",
        },
        {
            title: "一种简易的API加密方法",
            meta: {
                date: "APR 05, 2023",
                word_count: "662 Words",
                cover_img: "https://api.erdao.me/anipic?v=4"
            },
            description: "Lorem ipsum aasdad",
        },
        {
            title: "Typecho Mysql转Sqlite",
            meta: {
                date: "APR 05, 2023",
                word_count: "662 Words",
                cover_img: "https://api.erdao.me/anipic?v=5"
            },
            description: "Lorem ipsum aasdad",
        },
        {
            title: "深入理解计算机网络",
            meta: {
                date: "APR 06, 2023",
                word_count: "715 Words",
                cover_img: "https://api.erdao.me/anipic?v=6"
            },
            description: "Lorem ipsum dolor sit amet",
        },
        {
            title: "前端开发的最佳实践",
            meta: {
                date: "APR 07, 2023",
                word_count: "689 Words",
                cover_img: ""
            },
            description: "Lorem ipsum consectetuer adipiscing",
        },
        {
            title: "后端框架对比与分析",
            meta: {
                date: "APR 08, 2023",
                word_count: "653 Words",
                cover_img: "https://api.erdao.me/anipic?v=6"
            },
            description: "Lorem ipsum elit sed diam",
        },
        {
            title: "数据库性能优化技巧",
            meta: {
                date: "APR 09, 2023",
                word_count: "678 Words",
                cover_img: ""
            },
            description: "Lorem ipsum nonummy nibh euismod",
        }
    ]

    return PostMetas.slice(from, to);
}


export function fetchArticles(start, end) {
    return new Promise((resolve, reject) => {
        // Simulate fetching the post metadata, for example
        setTimeout(() => {
            resolve(request_article(start, end));
        }, 500); // for example, simulating variable fetch times
    });
}
