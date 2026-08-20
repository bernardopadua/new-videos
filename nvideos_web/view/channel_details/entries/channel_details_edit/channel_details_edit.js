export default class ChannelEditDetailsValidation {
    constructor() {
        this.channelDescription = document.getElementById("channelDescription");
        this.channelName = document.getElementById("channelName");

        this._alertValidationBlock = document.getElementById("channel-alert-validation-block");
        this.ulAlertList = document.getElementById("channel-warning-list");
    }

    clearValidationMessages() {
        while (this.ulAlertList.children.length > 1) {
            this.ulAlertList.lastElementChild.remove();
        }
        this.hideAlertBlock();
    }

    showAlertBlock() {
        this._alertValidationBlock.classList.remove("hidden");
    }

    hideAlertBlock() {
        this._alertValidationBlock.classList.add("hidden");
    }

    _addBulletAlert(alertMessage) {
        const liAlertMessage = document.createElement("li");
        liAlertMessage.className = "flex items-center gap-2";
        liAlertMessage.innerHTML = `<span class="text-xs text-amber-500/60">•</span><span class="text-white/70">${alertMessage}</span>`;
        this.ulAlertList.appendChild(liAlertMessage);
    }

    _validateChannelDescription() {
        const channelDescription = this.channelDescription.value;
        let valid = true;
        let alertMessage = "";

        if (channelDescription.length < 10) {
            valid = false;
            alertMessage = "Channel description must be at least 10 characters long.";
        }

        if (alertMessage) {
            this._addBulletAlert(alertMessage);
        }

        return valid;
    }

    _validateChannelName() {
        const channelName = this.channelName.value;
        let valid = true;
        let alertMessage = "";

        if (channelName.length < 3) {
            valid = false;
            alertMessage = "Channel name must be at least 3 characters long.";
        }

        if (alertMessage) {
            this._addBulletAlert(alertMessage);
        }

        return valid;
    }

    validateAllFields() {
        this.clearValidationMessages();

        const isDescriptionValid = this._validateChannelDescription();
        const isNameValid = this._validateChannelName();
        const isValid = isDescriptionValid && isNameValid;

        if (isValid) {
            this.hideAlertBlock();
        } else {
            this.showAlertBlock();
        }

        return isValid;
    }
};