from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
key = "YOUTUBE-API-KEY"

def get_channel_id_from_username(username):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={username}&key={key}"
    response = requests.get(url).json()
    if "items" in response and response["items"]:
        return response["items"][0]["snippet"]["channelId"]
    return None

def get_channel_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings,contentDetails&id={channel_id}&key={key}"
    response = requests.get(url).json()

    if "items" not in response or not response["items"]:
        return None

    data = response["items"][0]

    uploads_playlist_id = data.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads", None)
    latest_videos = get_latest_videos(uploads_playlist_id) if uploads_playlist_id else None

    return {
        "channel_name": data["snippet"]["title"],
        "channel_id": data["id"],
        "description": data["snippet"]["description"],
        "subscribers": data["statistics"]["subscriberCount"],
        "total_videos": data["statistics"]["videoCount"],
        "total_views": data["statistics"]["viewCount"],
        "thumbnail": data["snippet"]["thumbnails"]["high"]["url"],
        "country": data["brandingSettings"]["channel"].get("country", "Unknown"),
        "created_at": data["snippet"]["publishedAt"].split("T")[0],
        "banner_url": data["brandingSettings"]["image"].get("bannerExternalUrl", ""),
        "custom_url": data["snippet"].get("customUrl", ""),
        "latest_videos": latest_videos
    }

def get_latest_videos(playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=5&playlistId={playlist_id}&key={key}"
    response = requests.get(url).json()

    if "items" in response and response["items"]:
        videos = []
        for item in response["items"]:
            video = item["snippet"]
            videos.append({
                "title": video["title"],
                "video_id": video["resourceId"]["videoId"],
                "thumbnail": video["thumbnails"]["high"]["url"],
                "video_url": f"https://www.youtube.com/watch?v={video['resourceId']['videoId']}"
            })
        return videos
    return None

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Starexx YouTube API</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #d32f2f;
            --secondary-color: #e91e63;
            --text-color: #333;
            --font-family: 'Inter', sans-serif;
        }

        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: var(--font-family);
            background: #fff;
            color: var(--text-color);
            margin: 0;
            padding: 30px 20px;
        }

        h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        p {
            font-size: 16px;
            margin-bottom: 10px;
        }

        input {
            width: 95%;
            max-width: 400px;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 30px;
            font-size: 16px;
            font-family: var(--font-family);
            outline: none;
            margin-bottom: 10px;
            display: block;
            background: #fff;
            -webkit-user-select: text;
            user-select: text;
        }

        button {
            padding: 12px;
            width: 100%;
            max-width: 400px;
            border: none;
            border-radius: 30px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            font-weight: 600;
            font-size: 16px;
            font-family: var(--font-family);
            cursor: pointer;
            display: block;
            transition: opacity 0.3s ease;
        }

        button:hover {
            opacity: 0.8;
        }

        .footer {
            font-size: 14px;
            font-family: var(--font-family);
            opacity: 0.8;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <h1>Starexx</h1>
    <p>Enter a YouTube Username:</p>
    <input type="text" id="username" placeholder="Enter username (e.g., PewDiePie)">
    <button onclick="searchChannel()">Get Info</button>
    <p class="footer">Example: PewDiePie, MrBeast, etc.</p>

    <script>
        function searchChannel() {
            var username = document.getElementById('username').value.trim();
            if (username) {
                window.location.href = "/" + encodeURIComponent(username);
            }
        }
    </script>
</body>
</html>
    """)

@app.route("/<username>")
def youtube_info(username):
    channel_id = get_channel_id_from_username(username)
    if not channel_id:
        return jsonify({"error": "Channel not found"}), 404

    channel_data = get_channel_info(channel_id)
    if not channel_data:
        return jsonify({"error": "Channel not found"}), 404

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ channel_name }} (Starexx)</title>
            <style>
                :root {
                    --primary-color: #007bff;
                    --primary-hover-color: #0056b3;
                    --background-color: #f9f9f9;
                    --text-color: #333;
                    --container-bg: white;
                    --container-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    --border-radius: 10px;
                    --font-family: 'Inter', sans-serif;
                    -webkit-tap-highlight-color: transparent;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                }

                body {
                    font-family: var(--font-family);
                    margin: 0;
                    padding: 0;
                    text-align: left;
                    background-color: var(--background-color);
                    color: var(--text-color);
                }

                .banner {
                    width: 100%;
                    height: 150px;
                    background-size: cover;
                    background-position: center;
                }

                .container {
                    padding: 20px;
                    max-width: 800px;
                    margin: auto;
                    background: var(--container-bg);
                    border-radius: var(--border-radius);
                    box-shadow: var(--container-shadow);
                }

                .channel-info {
                    display: flex;
                    align-items: center;
                }

                .channel-info img {
                    width: 100px;
                    border-radius: 50%;
                    margin-right: 20px;
                }

                .details h1 {
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }

                .details span {
                    font-size: 16px;
                    color: gray;
                }

                .description {
                    font-size: 14px;
                    color: #555;
                    margin-top: 10px;
                }

                .stats {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 20px;
                    font-size: 14px;
                }

                .video {
                    margin-top: 20px;
                }

                .video img {
                    width: 100%;
                    height: auto;
                    max-height: 200px;
                    border-radius: 20px;
                    object-fit: cover;
                }

                .video a {
                    text-decoration: none;
                    color: var(--text-color);
                    font-weight: 600;
                }

                .footer {
                    margin-top: 20px;
                    text-align: center;
                    font-size: 14px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="banner" style="background-image: url('{{ banner_url }}');"></div>

            <div class="container">
                <div class="channel-info">
                    <img src="{{ thumbnail }}" alt="Channel Thumbnail">
                    <div class="details">
                        <h1>{{ channel_name }}</h1>
                        <span>Subscribers: {{ subscribers }}</span>
                    </div>
                </div>

                <p class="description">{{ description }}</p>

                <div class="stats">
                    <span><strong>Views:</strong> {{ total_views }}</span>
                    <span><strong>Country:</strong> {{ country }}</span>
                    <span><strong>Started:</strong> {{ created_at }}</span>
                </div>

                {% if latest_videos %}
                <div class="video">
                    <h3>Latest Videos:</h3>
                    {% for video in latest_videos %}
                    <div style="margin-bottom: 20px;">
                        <img src="{{ video.thumbnail }}" alt="Video Thumbnail">
                        <p><a href="{{ video.video_url }}" target="_blank">{{ video.title }}</a></p>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                <div class="footer">
                    <p>Powered by Starexx</p>
                </div>
            </div>
        </body>
        </html>
    """, **channel_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
