from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "X-IG-App-ID": "936619743392459"
}

def fetch_profile(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    response = requests.get(url, headers=HEADERS)
    return response

@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400
    
    response = fetch_profile(username)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500
    
    try:
        data = response.json().get("data", {}).get("user", {})
        if not data:
            return jsonify({"error": "User not found"}), 404

        posts = [
            {
                "Post ID": post["node"]["id"],
                "Caption": post["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                if post["node"]["edge_media_to_caption"]["edges"] else "No Caption",
                "Likes": post["node"]["edge_liked_by"]["count"],
                "Comments": post["node"]["edge_media_to_comment"]["count"],
                "Post URL": f"https://www.instagram.com/p/{post['node']['shortcode']}/",
                "Thumbnail": post["node"]["display_url"],
                "Type": "Video" if post["node"]["is_video"] else "Image"
            }
            for post in data.get("edge_owner_to_timeline_media", {}).get("edges", [])
        ]

        return jsonify({
            "Profile Info": {
                "Username": data.get("username"),
                "Full Name": data.get("full_name"),
                "Bio": data.get("biography"),
                "Followers": data.get("edge_followed_by", {}).get("count"),
                "Following": data.get("edge_follow", {}).get("count"),
                "Total Posts": data.get("edge_owner_to_timeline_media", {}).get("count"),
                "Profile Picture": data.get("profile_pic_url_hd"),
                "Private Account": data.get("is_private"),
            },
            "Recent Posts": posts
        })
    except Exception as e:
        return jsonify({"error": "Failed to parse response", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
