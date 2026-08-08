export default class VideoUploadFormValidation {
    constructor() {
        this._videoTitle = document.getElementById("videoTitle");
        this._videoDescription = document.getElementById("videoDescription");
        this._videoTags = document.getElementById("videoTags");

        this._ulList = document.getElementById("user-register-warning-list");
        this._alertValidationBlock = document.getElementById("user-register-form-alert");
    }

    showAlertBlock() {
        this._alertValidationBlock.classList.remove("hidden");
    }

    hideAlertBlock() {
        this._alertValidationBlock.classList.add("hidden");
    }

    clearValidationMessages() {
        while (this._ulList.children.length > 1) {
            this._ulList.lastElementChild.remove();
        }
        this.hideAlertBlock();
    }

    _addBulletAlert(alertMessage) {
        const _li = document.createElement("li");
        _li.className = "flex items-center gap-2";
        _li.innerHTML = `<span class="text-xs text-amber-500/60">•</span><span class="text-white/70">${alertMessage}</span>`;
        this._ulList.appendChild(_li);
    }

    validateAllFields() {
        const _validateVideoTitle = this._validateVideoTitle();
        const _validateVideoDescription = this._validateVideoDescription();
        const _validateVideoTags = this._validateVideoTags();
        const _validateThumbAndVideoFile = this._validateThumbAndVideoFile();
        const __allFieldsValid = (
            _validateVideoTitle && _validateVideoDescription &&
            _validateVideoTags && _validateThumbAndVideoFile
        );
        if (__allFieldsValid) {
            return true;
        }
        return false;
    }

    _validateVideoTitle() {
        const videoTitle = this._videoTitle.value.trim();
        if (videoTitle.length < 3) {
            this._addBulletAlert("Title must be at least 3 characters long.");
            return false;
        }
        return true;
    }

    _validateVideoDescription() {
        const videoDescription = this._videoDescription.value.trim();
        if (videoDescription.length < 20) {
            this._addBulletAlert("Description must be at least 20 characters long.");
            return false;
        }
        return true;
    }

    _validateVideoTags() {
        const videoTags = this._videoTags.value.trim();
        if (videoTags.length < 3) {
            this._addBulletAlert("You must inform at least 1 tag.");
            return false;
        }
        return true;
    }

    _validateThumbAndVideoFile() {
        const _videoThumbFile = document.getElementById("video_thumb_file");
        const _videoFile = document.getElementById("video_file");

        if (_videoThumbFile && _videoThumbFile.files.length === 0) {
            this._addBulletAlert("You must inform one thumb.");
            return false;
        }

        if (_videoFile && _videoFile.files.length === 0) {
            this._addBulletAlert("You must inform one video.");
            return false;
        }

        return true;
    }
    
};