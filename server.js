const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const FILE_DIR = path.join(__dirname, "src", "components");

// Home Route - JSON Response
app.get("/", (req, res) => {
    fs.readdir(FILE_DIR, (err, files) => {
        if (err) return res.status(500).json({ error: "Internal Server Error" });

        let fileList = files.map((file, index) => ({
            [index + 1]: `https://starexxx.vercel.app/${file}/`
        }));

        res.json({ Starexx: fileList });
    });
});

// Raw File Access Route
app.get("/:filename", (req, res) => {
    let requestedFile = req.params.filename;

    let filePath = path.join(FILE_DIR, requestedFile);
    if (fs.existsSync(filePath)) {
        res.setHeader("Content-Type", "text/plain");
        fs.createReadStream(filePath).pipe(res);
    } else {
        res.status(404).json({ error: "File doesn't exist" });
    }
});

// 405 Method Not Allowed
app.use((req, res, next) => {
    if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed" });
    next();
});

// 404 Not Found
app.use((req, res) => {
    res.status(404).json({ error: "Requested URL not Found" });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
