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

        # yt-dlp options
        ydl_opts = {'quiet': True, 'noplaylist': True}

        if format_choice == "audio":
            ydl_opts['format'] = 'bestaudio'
        elif format_choice == "video":
            ydl_opts['format'] = 'bestvideo'
        elif format_choice == "both":
            ydl_opts['format'] = 'best[ext=mp4]/best'  # Try finding pre-merged video

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if format_choice == "both":
                    video_url = info.get('url', None)
                    if not video_url:  # If no pre-merged video found, get separate streams
                        ydl_opts['format'] = 'bestvideo'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl_video:
                            video_info = ydl_video.extract_info(url, download=False)
                            video_url = video_info.get('url', None)

                        ydl_opts['format'] = 'bestaudio'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl_audio:
                            audio_info = ydl_audio.extract_info(url, download=False)
                            audio_url = audio_info.get('url', None)
                else:
                    video_url = info.get('url', None)

        except Exception as e:
            return f"Error: {str(e)}", 500

        return render_template("index.html", video_url=video_url, audio_url=audio_url)

    return render_template("index.html", video_url=None, audio_url=None)

if __name__ == "__main__":
    app.run(debug=True)
