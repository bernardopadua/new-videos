export default class ChannelImageUpload {
    constructor() {
        this._bannerImage = {
            obj: document.getElementById("channelBannerFile"),
            fileName: '',
            done: false
        };
        this._avatarImage = {
            obj: document.getElementById("channelAvatarFile"),
            fileName: '',
            done: false
        };
    }

    async uploadMedia(formData) {
        const urlToUpload = import.meta.env.VITE_URL_MEDIA_SERVER;
        try {
            if (this._bannerImage.obj.files.length > 0) {
                const formData = new FormData();
                formData.append("file", this._bannerImage.obj.files[0]);
                const responseBanner = await fetch(
                    urlToUpload + "/channel/upload/image/temp", {
                    method: "POST",
                    body: formData
                });
                const data = await responseBanner.json();
                this._bannerImage.fileName = data.filename;
                this._bannerImage.done = true;
            }
            if (this._avatarImage.obj.files.length > 0) {
                const formData = new FormData();
                formData.append("file", this._avatarImage.obj.files[0]);
                const responseAvatar = await fetch(
                    urlToUpload + "/channel/upload/image/temp", {
                    method: "POST",
                    body: formData
                });
                const data = await responseAvatar.json();
                this._avatarImage.fileName = data.filename;
                this._avatarImage.done = true;
            }
        } catch (e) {
            console.error(e);
        }
    }

    doUploadMedia(funcCallback) {
        this.uploadMedia().then(() => {
            if (this._bannerImage.done) {
                const bannerCoverUrl = document.getElementById("bannerCoverImageUrl");
                bannerCoverUrl.value = this._bannerImage.fileName;
            }
            if (this._avatarImage.done) {
                const avatarFileNameMediaServer = document.getElementById("avatarFileNameMediaServer")
                avatarFileNameMediaServer.value = this._avatarImage.fileName;
            }
            funcCallback();
        });
    }
};