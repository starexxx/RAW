const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "public"));
app.use(express.static("app"));

const FILE_DIR = path.join(__dirname, "src", "components");

app.get("/", (req, res) => {
    fs.readdir(FILE_DIR, (err, files) => {
        if (err) return res.status(500).send("Error reading directory");

        let fileList = files.map((file, index) => ({
            number: index + 1,
            name: file
        }));

        res.render("index", { files: fileList });
    });
});

app.get("/app/:filename", (req, res) => {
    let filePath = path.join(FILE_DIR, req.params.filename);

    if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        res.status(404).send("<h1>404 - File Not Found</h1>");
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
