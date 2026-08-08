import { ssrModuleExportsKey } from "vite/module-runner";

export default class VideoUploadService {
    constructor() {
        this._videoFile = document.getElementById("video_file");
        this._videoUUID = null;

        this._percent = 0;
        this._listeners = new Set();
    }

    getPercent = () => {
        return this._percent;
    }

    subscribe = (calllback) => {
        this._listeners.add(calllback);
        return () => { this._listeners.delete(calllback); }
    }

    setPercent(percent) {
        this._percent = percent;
        this._listeners.forEach(listener => {
            listener(this._percent);
        });
    }

    async initVideoUpload() {
        if (!this._videoFile) {
            this._videoFile = document.getElementById("video_file");
        }

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
        const jsonReturn = await this.uploadVideo();

        if (funcCallback) {
            funcCallback(jsonReturn);
        }
    }

    async getVideoUploadStatus() {
        if (!this._videoUUID) {
            await new Promise((resolve) => { setTimeout(resolve, 2000); });
            console.error("Error getVideoUploadStatus: video uuid is null");
            this.getVideoUploadStatus();
            return;
        }

        const urlGetStatus = import.meta.env.VITE_URL_MEDIA_SERVER + "/video/upload/status/" + this._videoUUID;
        const response = await fetch(urlGetStatus);
        
        if (!response.ok){
            console.error("Error get video upload status");
            return;
        }

        const r = await response.json();
        if (r.percent >= 0 && r.percent < 100) {
            this.setPercent(r.percent);
            await this.getVideoUploadStatus();
        } else if (r.percent == 100){
            this.setPercent(r.percent);
            return true;
        }
        return false;
    }
};