from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DUOME_URL = "https://duome.eu/{}/progress"

def get_duolingo_stats(username):
    url = DUOME_URL.format(username)
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    html = response.text

    # Extract streak 🔥
    streak_match = re.search(r"🔥 (\d+) day streak", html)
    streak = streak_match.group(1) if streak_match else "N/A"

    return {"username": username, "streak": streak}

@app.route('/duolingo/<username>', methods=['GET'])
def duolingo_stats(username):
    stats = get_duolingo_stats(username)
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
