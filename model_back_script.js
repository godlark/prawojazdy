{
    let video = document.querySelector(".media-wrapper video");
    if (video) {
        video.onloadedmetadata = () => {
            video.currentTime = video.duration - 0.01;
        };
    }
}