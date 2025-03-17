# Starexx RAW Uploads 

A simple Node.js and Express file server that lists files and serves them via URLs.

---

## Features  
- Lists all files inside the `/files` directory  
- Generates direct URLs for each file  
- Reads and serves text files  
- Supports automatic deployment on Vercel  

---

## Installation & Setup  

### Locally (Node.js)  
```bash
git clone https://github.com/starexxx/RAW.git
cd RAW
npm install
node index.js
```
---

### API Endpoints
**Example Response**

`GET /`
```json
{
  "Starexx": {
    "1": "https://starexxx.vercel.app/file1.txt/",
    "2": "https://starexxx.vercel.app/file2.txt/"
  }
}
```
`GET /file1.txt/`
<pre>
This is the content of file1.txt
</pre>

## License

This project is open-source and available under the [MIT License](License).




<p> </p>
<p align="center">
    <em><br><br>DEVELOPED BY <b>STAREXX</b></b></em>
</p>
