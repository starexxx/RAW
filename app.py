from flask import Flask, jsonify, send_from_directory, abort, redirect
import os

app = Flask(__name__)

FILES_DIR = "files"
BASE_URL = "https://starexxx.vercel.app"

@app.route('/')
def list_files():
    files = os.listdir(FILES_DIR)
    files_list = {str(i+1): f"{BASE_URL}/{file}/" for i, file in enumerate(files)}

    return jsonify({"Starexx": files_list}), 200

@app.route('/<filename>/')
def serve_file(filename):
    file_path = os.path.join(FILES_DIR, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File doesn't exist"}), 404

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}

@app.errorhandler(404)
def not_found(error):
    return redirect("/", code=302)  # Auto-redirect to home

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
