const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static("app"));

const FILE_DIR = path.join(__dirname, "src", "components");

// Home Route - JSON Response
app.get("/", (req, res) => {
    fs.readdir(FILE_DIR, (err, files) => {
        if (err) {
            return res.status(500).json({ error: "Internal Server Error" });
        }

        let fileList = files.map((file, index) => ({
            [index + 1]: `https://starexxx.vercel.app/${path.parse(file).name}/`
        }));

        res.json({ Starexx: fileList });
    });
});

// File Access Route
app.get("/:filename", (req, res) => {
    let requestedFile = req.params.filename;

    fs.readdir(FILE_DIR, (err, files) => {
        if (err) {
            return res.status(500).json({ error: "Internal Server Error" });
        }

        let matchingFile = files.find(file => path.parse(file).name === requestedFile);

        if (matchingFile) {
            res.sendFile(path.join(FILE_DIR, matchingFile));
        } else {
            res.status(404).json({ error: "File doesn't exist" });
        }
    });
});

// Handle Unsupported Methods
app.use((req, res, next) => {
    if (req.method !== "GET") {
        return res.status(405).json({ error: "Method not allowed" });
    }
    next();
});

// 404 Error for Invalid Routes
app.use((req, res) => {
    res.status(404).json({ error: "Requested URL not Found" });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
