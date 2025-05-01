from flask import Flask, request, jsonify

app = Flask(__name__)
from llama_agent import highlight_clips
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["discord_ai"]

@app.route("/save", methods=["POST"])
def save_transcript():
    data = request.get_json(force=True)
    db.transcripts.insert_one({"url": data["audio_url"],
                               "text": data["transcript"]})
    return jsonify({"ok": True})


@app.route("/highlight", methods=["POST"])
def highlight_route():
    data = request.get_json(force=True)
    transcript = data.get("transcript", "")
    picks = highlight_clips(transcript)
    return jsonify({"highlights": picks})


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500


@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json(force=True)
    audio_url = data.get("audio_url")
    # TODO: run transcription (stubbed)
    transcript = f"[fake transcript of {audio_url}]"
    return jsonify({"transcript": transcript})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
