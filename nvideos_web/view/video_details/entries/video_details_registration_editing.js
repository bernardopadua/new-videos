import VideoUploadService from './video_upload/video_upload';

const videoForm = document.getElementById("video-form");
export const videoUploadService = new VideoUploadService();
videoForm.addEventListener("submit", (e) => {
    e.preventDefault();

    
    /*videoUploadService.doVideoUpload((r) => {
        console.log("video finished");
    });*/
    videoUploadService.initVideoUpload();
    videoUploadService.getVideoUploadStatus((r) => {
        console.log('finished percent:: ', r);
    });
});