from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():
    youtube_url = request.form.get("url")
    resolution = request.form.get("resolution")
    total_size = 0

    def display_progress(chunk, file_handler, bytes_remaining):
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print(f"Downloaded: {percentage:.2f}% - {bytes_downloaded}/{total_size} bytes")

    # Download the video
    try:
        yt = YouTube(youtube_url, on_progress_callback=display_progress)
        video = yt.streams.filter(res=resolution, progressive=True).first()
        total_size = video.filesize
        if video:
            video.download(output_path="videos-inputs")
            # Super resolution with Real-esrgan
            os.system(
                f"python3 real-esrgan/inference_realesrgan_video.py -i video-inputs -n realesrgan-x4plus -s 2 --suffix outx2 -o video-outputs"
            )
            return redirect(url_for("index"))
        else:
            return "Video with the specified resolution not found."

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
