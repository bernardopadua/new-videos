export default class ThumbnailUploadService {
    async doUploadThumbnail(){
        const thumbFile = document.getElementById("video_thumb_file");

        if (!thumbFile){
            console.error("Error uploading thumbnail: video_thumb_file is null");
            return;
        }

        const file = thumbFile.files[0];
        if (!file){
            console.error("Error uploading thumbnail: file is null");
            return;
        }

        const formData = new FormData();
        const urlUpload = import.meta.env.VITE_URL_MEDIA_SERVER + "/video/upload/thumb/temp"
        
        formData.append("video_thumb_file", file);

        const response = await fetch(urlUpload, {
            method: "POST",
            body: formData
        });

        if (!response.ok){
            console.error("Error uploading thumbnail: response is not ok");
            return;
        }

        return response.json();
    }

    checkFilesToUpload(){
        const thumbFile = document.getElementById("video_thumb_file");
        if (!thumbFile) return false;
        return thumbFile.files.length > 0;
    }
};