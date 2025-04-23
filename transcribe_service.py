from flask import Flask, request, jsonify

app = Flask(__name__)

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
