const express = require('express');
const path = require('path');
const compression = require('compression');
const svgCaptcha = require('svg-captcha');


const app = express();
const PORT = 3000;

app.use(compression());

// Serve static files from the 'assets' directory
app.use('/assets', express.static('assets'));


app.get('/captcha', function (req, res) {
	var captcha = svgCaptcha.create();
	// req.session.captcha = captcha.text;
	
	res.type('svg');
	res.status(200).send(captcha.data);
});

app.get('/', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'));
});

app.get('/about', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'));
});

app.get('/post', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'post.html'));
});

app.get('/article/:id', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'));
});



app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
