def highlight_clips(transcript: str):
    """
    Simple stub: split transcript into sentences and rank them by length.
    Later, plug in LLaMA model here.
    """
    parts = [p.strip() for p in transcript.split(".") if p.strip()]
    ranked = sorted(parts, key=len, reverse=True)
    return ranked[:3]  # top 3 highlights

if __name__ == "__main__":
    txt = "Player scored. Big combo! Amazing teamwork."
    print(highlight_clips(txt))
