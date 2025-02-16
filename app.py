import os
from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_url = None
    audio_url = None

    if request.method == "POST":
        url = request.form.get("url")
        format_choice = request.form.get("format")

        if not url:
            return "Please enter a YouTube URL", 400

        # Load cookies from a file
        cookies_path = "static/cookies_youtube.txt"
        if not os.path.exists(cookies_path):
            return "Cookies file not found!", 500

        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'cookies': cookies_path,  # Load YouTube cookies
        }

        if format_choice == "audio":
            ydl_opts['format'] = 'bestaudio'
        elif format_choice == "video":
            ydl_opts['format'] = 'bestvideo'
        elif format_choice == "both":
            ydl_opts['format'] = 'best[ext=mp4]/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url', None)

        except Exception as e:
            return f"Error: {str(e)}", 500

        return render_template("index.html", video_url=video_url)

    return render_template("index.html", video_url=None)

if __name__ == "__main__":
    app.run(debug=True)
