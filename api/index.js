const fs = require("fs");
const path = require("path");

module.exports = async (req, res) => {
    if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed" });

    const FILE_DIR = path.join(__dirname, "..", "src", "components");

    if (req.url === "/api/files") {
        try {
            if (!fs.existsSync(FILE_DIR)) return res.json({ Starexx: [] });

            let files = fs.readdirSync(FILE_DIR);
            let fileList = files.map((file, index) => ({
                [index + 1]: `https://starexxx.vercel.app/${path.parse(file).name}/`
            }));

            return res.json({ Starexx: fileList });
        } catch (err) {
            return res.status(500).json({ error: "Internal Server Error" });
        }
    }

    // Serve raw file content
    const fileName = decodeURIComponent(req.url.slice(1));
    const filePath = path.join(FILE_DIR, fileName + ".html");

    if (fs.existsSync(filePath)) {
        res.setHeader("Content-Type", "text/html");
        return res.end(fs.readFileSync(filePath));
    }

    return res.status(404).json({ error: "Requested URL not Found" });
};
