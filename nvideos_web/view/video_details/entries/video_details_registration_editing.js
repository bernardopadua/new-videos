import VideoUploadService from './video_upload/video_upload';
import ThumbnailUploadService from './video_upload/thumbnail_upload';
import VideoUploadFormValidation from './vide_details_form_validation';

class MediaUploadAlertService {
    constructor() {
        this._mediaUploadAlert = document.getElementById("media-upload-alert");
        this._mediaUploadAlertError = document.getElementById("media-upload-alert-error");
    }

    showLoading() {
        if (this._mediaUploadAlert) this._mediaUploadAlert.classList.remove("hidden");
        if (this._mediaUploadAlertError) this._mediaUploadAlertError.classList.add("hidden");
    }

    hideLoading() {
        if (this._mediaUploadAlert) this._mediaUploadAlert.classList.add("hidden");
        if (this._mediaUploadAlertError) this._mediaUploadAlertError.classList.add("hidden");
    }

    showError() {
        if (this._mediaUploadAlert) this._mediaUploadAlert.classList.add("hidden");
        if (this._mediaUploadAlertError) this._mediaUploadAlertError.classList.remove("hidden");
    }
};

const videoForm = document.getElementById("video-form");
export const videoUploadService = new VideoUploadService();
const thumbnailUploadService = new ThumbnailUploadService();
const videoUploadFormValidation = new VideoUploadFormValidation();
videoForm.addEventListener("submit", (e) => {
    e.preventDefault();

    videoUploadFormValidation.clearValidationMessages();
    if (!videoUploadFormValidation.validateAllFields()) {
        videoUploadFormValidation.showAlertBlock();
        return;
    }

    const mediaUploadAlert = new MediaUploadAlertService();

    mediaUploadAlert.showLoading();
    document.getElementById("media-upload-alert").scrollIntoView({ behavior: 'smooth', block: 'center' });
    //I opted to upload the thumb first, not complicated management.
    //Simple that works.
    thumbnailUploadService.doUploadThumbnail().then(r => {
        const videoThumbTempFilename = document.getElementById('videoThumbTempFilename');
        if (videoThumbTempFilename) {
            videoThumbTempFilename.value = r.filename;
        } else {
            console.error("Error getting temp video thumb filename");
            console.error("Aborting video upload.");
            mediaUploadAlert.showError();
            return;
        }

        const getTempVideoFileName = (r) => {
            const videoTempFileName = document.getElementById('videoTempFilename');
            if (!videoTempFileName) {
                console.error("Error getVideoUploadStatus: video uuid is null");
                mediaUploadAlert.showError();
                return;
            }
            if (r && r.filename) {
                videoTempFileName.value = r.filename;
            } else {
                mediaUploadAlert.showError();
                return;
            }

            mediaUploadAlert.hideLoading();
            videoForm.submit();
        };

        videoUploadService.doVideoUpload(getTempVideoFileName);
        videoUploadService.getVideoUploadStatus();
    });
    
});