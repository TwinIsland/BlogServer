const express = require('express');
const path = require('path');


const app = express();
const PORT = 3000;

// Serve static files from the 'assets' directory
app.use('/assets', express.static('assets'));


app.get('/', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'));
});

app.get('/about', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
