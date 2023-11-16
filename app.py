from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from pytube import YouTube
import shutil
import shlex
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
            video_input_path = video.download(output_path="video-inputs").replace(
                " ", "fsdf"
            )
            # Super resolution
            shutil.copy(video_input_path, f"video-outputs/output_video.mp4")
            print(
                f"calling: python real-esrgan/inference_realesrgan_video.py -i {video_input_path} -n RealESRGAN_x4plus -s 2 --suffix outx2 -o video-outputs --fp32"
            )
            os.system(
                f"python real-esrgan/inference_realesrgan_video.py -i {video_input_path} -n RealESRGAN_x4plus -s 2 --suffix outx2 -o video-outputs --fp32"
            )
            # Display video

            return redirect(url_for("watch_video", filename="output_video.mp4"))
        else:
            return "Video with the specified resolution not found."

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/video-outputs/<filename>")
def watch_video(filename):
    return send_from_directory("video-outputs", filename)


if __name__ == "__main__":
    app.run(debug=True)
