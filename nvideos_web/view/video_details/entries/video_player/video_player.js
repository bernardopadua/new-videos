import { ROUTES } from "../../../base/entries/constants/routes";

export default function VideoPlayerInit() {
    const videoKey = JSON.parse(document.getElementById("initial-data").innerText)?.videoKey;
    const videoPlayer = document.getElementById("main-video-player");
    const videoSource = `${import.meta.env.VITE_URL_MEDIA_SERVER}${ROUTES.videoWatchMediaServer(videoKey)}`;

    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(videoSource);
        hls.attachMedia(videoPlayer);
    } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
        videoPlayer.src = videoSource;
    }
};