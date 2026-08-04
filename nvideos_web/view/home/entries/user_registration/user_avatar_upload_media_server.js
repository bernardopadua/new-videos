export default class AvatarUploadMediaServer {
    constructor() {
        this._avatar = document.getElementById("userAvatar");
    }

    async uploadMedia(formData) {
        const urlToUpload = import.meta.env.VITE_URL_MEDIA_SERVER;
        
        const response = await fetch(urlToUpload+"upload/avatar/temp", {
            method: "POST",
            body: formData
        }).then(
            response => {
                return response.json();
            }
        );

        if (response.status != 200) {
            return;
        }

        return response.data;
    }

    doUploadAvatar() {
        if (this.checkFilesSelected()) {
            const formData = new FormData();
            formData.append("avatarImage", this._avatar.files[0]);
            this.uploadMedia(formData);
        }
    }

    checkFilesSelected() {
        return this._avatar.files.length > 0;
    }
};