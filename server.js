const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.static("app"));

const FILE_DIR = path.join(__dirname, "src", "components");

app.get("/:filename", (req, res) => {
    let requestedFile = req.params.filename;
    
    fs.readdir(FILE_DIR, (err, files) => {
        if (err) return res.status(500).send("Error reading directory");

        let matchingFile = files.find(file => path.parse(file).name === requestedFile);
        
        if (matchingFile) {
            res.sendFile(path.join(FILE_DIR, matchingFile));
        } else {
            res.status(404).send("<h1>404 - File Not Found</h1>");
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
