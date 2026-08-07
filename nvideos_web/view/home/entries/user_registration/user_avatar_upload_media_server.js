export default class AvatarUploadMediaServer {
    constructor() {
        this._avatar = document.getElementById("userAvatar");
        this._responseUploadJson = {};
    }

    async uploadMedia(formData) {
        const urlToUpload = import.meta.env.VITE_URL_MEDIA_SERVER;
        
        try {
            const response = await fetch(urlToUpload + "/upload/avatar/temp", {
                method: "POST",
                body: formData
            });

            if (response.status != 200) {
                return false;
            }

            return response.json();
        } catch (error) {
            return false;
        }
    }

    doUploadAvatar() {
        if (this.checkFilesSelected()) {
            const formData = new FormData();
            formData.append("avatarImage", this._avatar.files[0]);
            return this.uploadMedia(formData);
        }
        return false;
    }

    checkFilesSelected() {
        return this._avatar.files.length > 0;
    }
};