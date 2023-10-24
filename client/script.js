// script.js

const video = document.getElementById('sourceVideo');
const canvas = document.getElementById('outputCanvas');
const ctx = canvas.getContext('2d');
const progressBar = document.getElementById('progressBar');
const playButton = document.getElementById('playButton');
const pauseButton = document.getElementById('pauseButton');

video.addEventListener('play', function () {
    const loop = function () {
        if (!video.paused && !video.ended) {
            drawFrame();
            setTimeout(loop, 1000 / 30); // Draw at 30 FPS
        }
    };
    loop();
}, false);

video.addEventListener('timeupdate', function () {
    let percentage = (video.currentTime / video.duration) * 100;
    progressBar.style.width = percentage + "%";
});

function drawFrame() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    let data = imageData.data;
    console.log(data)
    for (let i = 0; i < data.length; i += 4) {
        let avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = avg; // red
        data[i + 1] = avg; // green
        data[i + 2] = avg; // blue
    }
    ctx.putImageData(imageData, 0, 0);
}

// If you have play and pause buttons:
playButton.addEventListener('click', function () {
    video.play();
});
pauseButton.addEventListener('click', function () {
    video.pause();
});
