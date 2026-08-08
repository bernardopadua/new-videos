import VideoUploadService from './video_upload/video_upload';
import ThumbnailUploadService from './video_upload/thumbnail_upload';

const videoForm = document.getElementById("video-form");
export const videoUploadService = new VideoUploadService();
const thumbnailUploadService = new ThumbnailUploadService();
videoForm.addEventListener("submit", (e) => {
    e.preventDefault();

    //I opted to upload the thumb first, not complicated management.
    //Simple that works.
    thumbnailUploadService.doUploadThumbnail().then(r => {
        const videoThumbTempFilename = document.getElementById('videoThumbTempFilename');
        if (videoThumbTempFilename) {
            videoThumbTempFilename.value = r.filename;
        } else {
            console.error("Error getting temp video thumb filename");
            console.error("Aborting video upload.")
            return;
        }

        const getTempVideoFileName = (r) => {
            const videoTempFileName = document.getElementById('videoTempFilename');
            if (!videoTempFileName) {
                console.error("Error getVideoUploadStatus: video uuid is null");
                return;
            }
            videoTempFileName.value = r.filename;

            videoForm.submit();
        };
        
        videoUploadService.doVideoUpload(getTempVideoFileName);
        videoUploadService.getVideoUploadStatus();
    });
    
});