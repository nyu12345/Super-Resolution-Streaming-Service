from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define the directory to store uploaded videos
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    # List all video files in the 'uploads' directory
    video_files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", video_files=video_files)


@app.route("/upload", methods=["POST"])
def upload():
    # Check if the post request has the file part
    if "video" not in request.files:
        return redirect(request.url)

    video_file = request.files["video"]

    # Check if the user submitted an empty form
    if video_file.filename == "":
        return redirect(request.url)

    # Check if the file is an allowed video format (e.g., .mp4)
    if video_file and video_file.filename.endswith(".mp4"):
        video_file.save(os.path.join(app.config["UPLOAD_FOLDER"], video_file.filename))

    return redirect(url_for("index"))


@app.route("/play/<filename>")
def play(filename):
    return render_template("play.html", filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
