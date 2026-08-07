class VideoUploadService {
    constructor() {
        this._videoFile = document.getElementById("video_file");
        this._videoUUID = null;
    }

    async initVideoUpload() {
        const urlToUpload = import.meta.env.VITE_URL_MEDIA_SERVER;
        const file = this._videoFile.files[0];

        const response = await fetch(urlToUpload + "/video/init/upload", {
            method: "POST",
            body: JSON.stringify({
                fileName: file.name,
                fileSize: file.size
            }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        
        if (!response.ok){
            console.error("Error init video upload");
            return;
        }

        this._videoUUID = (await response.json()).uuid;  
    }

    async uploadVideo() {
        const formData = new FormData();
        formData.append("file", this._videoFile.files[0]);

        const urlToUpload = import.meta.env.VITE_URL_MEDIA_SERVER + "/video/upload/"+this._videoUUID;
        const response = await fetch(urlToUpload, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            console.error("Error upload video");
            return;
        }

        return response.json();
    }
    
    async doVideoUpload(funcCallback = null) {
        await this.initVideoUpload();
        this.uploadVideo().then((r) => {
            if (funcCallback) {
                funcCallback(r);
            }
        });
    }

    async getVideoUploadStatus(funcCallback = null) {
        const urlGetStatus = import.meta.env.VITE_URL_MEDIA_SERVER + "/video/upload/status/" + this._videoUUID;
        const response = await fetch(urlGetStatus);
        
        if (!response.ok){
            console.error("Error get video upload status");
            return;
        }

        const r = await response.json();
        if (r.percent != 100) {
            if (funcCallback) {
                funcCallback();
            }
            this.getVideoUploadStatus(funcCallback);
        }
    }
}