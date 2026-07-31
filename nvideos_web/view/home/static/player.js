const video = document.getElementById('video');
const videoSrc = 'http://localhost:8099/video/k9X7p2M4w8L/playlist.m3u8'; // Substitua pela sua URL .m3u8

if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
} 
// Fallback para Safari/iOS (que já suportam HLS nativamente no HTML5)
else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = videoSrc;
}