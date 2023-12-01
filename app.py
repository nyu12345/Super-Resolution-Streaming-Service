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
    upscaling = request.form.get("upscaling")
    model = request.form.get("model")
    face = request.form.get("face")
    total_size = 0

    def display_progress(chunk, file_handler, bytes_remaining):
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print(f"Downloaded: {percentage:.2f}% - {bytes_downloaded}/{total_size} bytes")

    # Download the video
    try:
        ## remove all existing videos
        os.system("rm static/video-inputs/*")
        os.system("rm static/video-outputs/*")

        ## download video from youtube
        yt = YouTube(youtube_url, on_progress_callback=display_progress)
        video = yt.streams.filter(
            res=resolution, progressive=True, file_extension="mp4"
        ).first()
        if video:
            total_size = video.filesize
            video_input_path = video.download(
                output_path="static/video-inputs",
                filename=video.title.replace(" ", "_") + ".mp4",
            )
            ## Super resolution
            os.system(
                f"python real-esrgan/inference_realesrgan_video.py -i {shlex.quote(video_input_path)} --fp32 -n {model} -s {upscaling} {face} --suffix outx2 -o static/video-outputs"
            )

            # Display video

            return redirect(
                url_for(
                    "watch_videos",
                    original=os.path.basename(video_input_path),
                    super_res=video.title.replace(" ", "_") + "_outx2.mp4",
                )
            )
        else:
            return ".mp4 video with the specified resolution not found."

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/watch_videos")
def watch_videos():
    return render_template(
        "watch_videos.html",
        original=request.args.get("original"),
        super_res=request.args.get("super_res"),
    )


if __name__ == "__main__":
    app.run(debug=True)
