import { VideoUploadService } from "./video_upload/video_upload.js";

const videoForm = document.getElementById("video-form");
videoForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const videoUploadService = new VideoUploadService();
    videoUploadService.doVideoUpload((r) => {
        console.log("video finished");
    });
    videoUploadService.getVideoUploadStatus(() => {
        console.log("Update percent");
    });
});