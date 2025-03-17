const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const FILES_DIR = "files";
const BASE_URL = "https://starexxx.vercel.app";

app.get("/", (req, res) => {
    fs.readdir(FILES_DIR, (err, files) => {
        if (err) {
            res.set("X-Title", "Error");
            return res.status(500).json({ error: "Internal Server Error" });
        }

        let filesList = {};
        files.forEach((file, index) => {
            filesList[index + 1] = `${BASE_URL}/${file}/`;
        });

        res.set("X-Title", "Starexx File List");
        res.status(200).json({ "Starexx": filesList });
    });
});

app.get("/:filename/", (req, res) => {
    const filePath = path.join(FILES_DIR, req.params.filename);

    if (!fs.existsSync(filePath)) {
        res.set("X-Title", "404 Not Found");
        return res.status(404).json({ error: "File doesn't exist" });
    }

    fs.readFile(filePath, "utf8", (err, data) => {
        if (err) {
            res.set("X-Title", "Error Reading File");
            return res.status(500).json({ error: "Error reading file" });
        }
        res.set("X-Title", req.params.filename);
        res.type("text/plain").send(data);
    });
});

app.use((req, res) => {
    res.set("X-Title", "Redirecting...");
    res.redirect("/");
});

app.listen(8000, () => {
    console.log("Server is running on http://0.0.0.0:8000");
});
