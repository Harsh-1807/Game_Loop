from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the file that will store the high score
HIGH_SCORE_FILE = 'high_score.json'

# Ensure the file exists with a default high score
if not os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({"highScore": 0}, f)

def get_high_score():
    """Retrieve the current high score from the file."""
    with open(HIGH_SCORE_FILE, 'r') as f:
        data = json.load(f)
    return data.get('highScore', 0)

def set_high_score(score):
    """Set a new high score to the file if it's higher than the current one."""
    current_high_score = get_high_score()
    if score > current_high_score:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({"highScore": score}, f)
        return score
    return current_high_score

@app.route('/high-scores', methods=['GET'])
def get_high_scores():
    """API endpoint to get the high score."""
    return jsonify({"highScore": get_high_score()})

@app.route('/high-scores', methods=['POST'])
def post_high_score():
    """API endpoint to update the high score."""
    data = request.get_json()
    score = data.get('score')
    if score is not None:
        new_high_score = set_high_score(score)
        return jsonify({"highScore": new_high_score})
    return jsonify({"error": "No score provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
