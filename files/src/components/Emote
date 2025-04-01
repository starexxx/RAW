<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <title>Emotes</title>
    <style>
        :root {
            --bg-color: rgba(0, 0, 0);
            --icon-bg: rgba(19, 19, 19);
            --popup-bg: rgba(30, 30, 30);
            --text-color: rgba(255, 255, 255);
            --button-bg: rgba(80, 167, 234);
            --button-text: rgba(255, 255, 255);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 10px;
            padding: 20px;
            max-width: 600px;
            width: 100%;
        }

        .icon-box {
            width: 120px;
            height: 120px;
            background: var(--icon-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            cursor: pointer;
            overflow: hidden;
        }

        .icon-box img {
            max-width: 90px;
            max-height: 90px;
            object-fit: contain;
            opacity: 0;
            transform: scale(0.8);
            transition: opacity 0.4s ease-out, transform 0.3s ease-out;
        }

        .icon-box img.loaded {
            opacity: 1;
            transform: scale(1);
        }

        .popup {
            position: fixed;
            bottom: -105%;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 450px;
            background: var(--popup-bg);
            color: var(--text-color);
            padding: 15px;
            border-radius: 20px 20px 0 0;
            text-align: center;
            transition: bottom 0.3s ease-in-out;
        }

        .popup img {
            width: 100px;
            height: 130px;
            margin-bottom: 10px;
        }

        .popup h3 {
            margin: 5px 0;
            font-size: 18px;
        }

        .popup p {
            margin: 5px 0;
            font-size: 14px;
            color: #aaa;
            user-select: text;
        }

        .popup button {
            font-family: 'Inter', sans-serif;
            margin-top: 10px;
            width: 100%;
            padding: 13px;
            border: none;
            background: var(--button-bg);
            color: var(--button-text);
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }

        .popup button:hover {
            background: #3c8cd2;
        }

        .popup button:active {
            transform: scale(0.95);
        }

        .show-popup {
            bottom: 0;
        }

        ::selection {
            background-color: var(--icon-bg);
            color: var(--text-color);
        }
    </style>
</head>
<body>
    <h2><br>Starexx Emotes<br></h2>
    <div class="container" id="iconContainer"></div>

    <div class="popup" id="popup">
        <img id="popupIcon" src="" alt="Icon">
        <h3 id="popupTitle">Name</h3>
        <p id="popupItemID">Item ID: 000000</p>
        <button onclick="closePopup()">OK</button>
    </div>

    <script>
        const URL = "https://raw.githubusercontent.com/starexxx/starexxx/refs/heads/main/app.json";
        const ICON_URL = "https://system.ffgarena.cloud/api/iconsff?image=";
        const DEFAULT_ICON = "https://system.ffgarena.cloud/api/iconsff?image=1001000100.png";

        function getSearchQuery() {
            const params = new URLSearchParams(window.location.search);
            return params.get("q") ? decodeURIComponent(params.get("q")) : null;
        }

        async function fetchIcons() {
            try {
                const response = await fetch(URL);
                if (!response.ok) throw new Error("File not found");
                const data = await response.json();
                const iconsData = data.filter(item => item["Icon_Name"].startsWith("Icon_Name_Emote"));

                const searchQuery = getSearchQuery();
                const container = document.getElementById("iconContainer");
                container.innerHTML = "";

                let filteredIcons = iconsData;
                if (searchQuery) {
                    filteredIcons = iconsData.filter(item => item.Name.toLowerCase().includes(searchQuery.toLowerCase()));
                }

                if (filteredIcons.length === 0) {
                    container.innerHTML = `<p>No emotes found for "${searchQuery}"</p>`;
                    return;
                }

                filteredIcons.forEach(item => {
                    const div = document.createElement("div");
                    div.classList.add("icon-box");

                    const img = document.createElement("img");
                    img.src = `${ICON_URL}${item.Item_ID}.png`;
                    img.onerror = () => { img.src = DEFAULT_ICON; };

                    img.onload = () => {
                        img.classList.add("loaded");
                    };

                    div.appendChild(img);
                    div.onclick = () => openPopup(item.Name, item.Item_ID, img.src);

                    container.appendChild(div);
                });
            } catch (error) {
                console.error("Error fetching data:", error);
                document.getElementById("iconContainer").innerHTML = `<p>Error loading emotes.</p>`;
            }
        }

        function openPopup(name, id, imgSrc) {
            document.getElementById("popupTitle").textContent = name;
            document.getElementById("popupItemID").textContent = "Item ID: " + id;
            document.getElementById("popupIcon").src = imgSrc;
            document.getElementById("popup").classList.add("show-popup");
        }

        function closePopup() {
            document.getElementById("popup").classList.remove("show-popup");
        }

        fetchIcons();
    </script>
</body>
</html>
