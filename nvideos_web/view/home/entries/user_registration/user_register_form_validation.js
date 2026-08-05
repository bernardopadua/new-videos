import AvatarUploadMediaServer from "./user_avatar_upload_media_server.js"

class UserRegistrationValidator {
    constructor() { 
        this._userName = document.getElementById("userName");
        this._userSurname = document.getElementById("userSurname");
        this._userEmail = document.getElementById("userEmail");
        this._birthDate = document.getElementById("birthDate");
        this._userPassword = document.getElementById("userPassword");
        this._confirmPassword = document.getElementById("confirmPassword");
        this._terms = document.getElementById("terms");

        this._alert = document.getElementById("user-register-form-alert");
    }

    _resetBulletAlert() {
        const ulAlert = document.getElementById("user-register-warning-list");
        const liDefault = document.createElement("li");
        liDefault.classList.add("flex", "items-center", "gap-2");
        liDefault.innerHTML = `
            <span class="text-xs text-amber-600/60">•</span>
            <span class="text-red-400">Attention: Please check the errors below.</span>
        `;
        ulAlert.innerHTML = "";
        ulAlert.appendChild(liDefault);
    }

    _addBulletAlert(alertMessage) {
        const ulAlert = document.getElementById("user-register-warning-list");
        const li = document.createElement("li");
        li.classList.add("flex", "items-center", "gap-2");
        li.innerHTML = `
            <span class="text-xs text-amber-600/60">•</span>
            <span>${alertMessage}</span>
        `;
        ulAlert.appendChild(li);
    }

    validateAllFields() {
        this._alert.classList.add("hidden");
        this._resetBulletAlert();
        
        const userNameValidated = this._validateUserName();
        const userSurnameValidated = this._validateUserSurname();
        const userEmailValidated = this._validateUserEmail();
        const birthDateValidated = this._validateBirthDate();
        const userPasswordValidated = this._validateUserPassword();
        const confirmPasswordValidated = this._validateConfirmPassword();
        const spacesInPasswordValidated = this._validateSpacesInPassword();
        const ageValidation = this._validateAge();

        if (!(
            userNameValidated &&
            userSurnameValidated &&
            userEmailValidated &&
            birthDateValidated &&
            userPasswordValidated &&
            confirmPasswordValidated &&
            spacesInPasswordValidated &&
            ageValidation
        )) {
            this._alert.classList.remove("hidden");
            return false;
        }

        return true;
    }

    _validateAge() {
        const birthDate = String(this._birthDate.value);
        const age = new Date().getFullYear() - parseInt(birthDate.split('-')[0]);
        if (age >= 18) {
            return true;
        }

        this._addBulletAlert("You must be at least 18 years old.");
        return false;
    }

    _validateUserName() {
        const userName = this._userName.value.trim();
        if (userName.length < 3) {
            this._addBulletAlert("Name must be at least 3 characters long.");
            return false;
        }
        return true;
    }

    _validateUserSurname() {
        const userSurname = this._userSurname.value.trim();
        if (userSurname.length < 3) {
            this._addBulletAlert("Surname must be at least 3 characters long.");
            return false;
        }
        return true;
    }

    _validateUserEmail() {
        const userEmail = this._userEmail.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(userEmail)) {
            this._addBulletAlert("Email is invalid.");
            return false;
        }

        return true;
    }

    _validateBirthDate() {
        const birthDate = this._birthDate.value;
        if (!birthDate) {
            this._addBulletAlert("Date of birth is required.");
            return false;
        }
        return true;
    }

    _validateUserPassword() {
        const userPassword = this._userPassword.value.trim();
        if (userPassword.length < 6) {
            this._addBulletAlert("Password must be at least 6 characters long.");
            return false;
        }
        return true;
    }

    _validateSpacesInPassword() {
        const userPassword = this._userPassword.value;
        if (userPassword.includes(" ")) {
            this._addBulletAlert("Password cannot contain spaces.");
            return false;
        }
        return true;
    }
    
    _validateConfirmPassword() {
        const confirmPassword = this._confirmPassword.value;
        const userPassword = this._userPassword.value;
        if (confirmPassword !== userPassword) {
            this._addBulletAlert("Passwords do not match.");
            return false;
        }
        return true;
    }
};

const disableRegistrationButton = () => {
    document.getElementById("btn-submit-register").classList.add("disabled:opacity-50", "disabled:cursor-not-allowed", "disabled:pointer-events-none");
};

const enableRegistrationButton = () => {
    document.getElementById("btn-submit-register").classList.remove("disabled:opacity-50", "disabled:cursor-not-allowed", "disabled:pointer-events-none");
};

const formUserRegister = document.getElementById("register-form");
formUserRegister.addEventListener("submit", (event) => {
    event.preventDefault();
    disableRegistrationButton();

    const userRegistrationValidator = new UserRegistrationValidator();
    const userAvatarUpload = new AvatarUploadMediaServer();
    const allFieldsAreValidated = userRegistrationValidator.validateAllFields();

    if (
        userAvatarUpload.checkFilesSelected()
        && allFieldsAreValidated
        && document.getElementById("avatarFileNameMediaServer").value === ""
    ) {
        document.getElementById("avatar-upload-alert-error").classList.add("hidden");
        document.getElementById("avatar-upload-alert").classList.remove("hidden");

        userAvatarUpload.doUploadAvatar().then((result) => {
            if (!result) {
                document.getElementById("avatar-upload-alert-error").classList.remove("hidden");
                document.getElementById("avatar-upload-alert").classList.add("hidden");
            } else {
                document.getElementById("avatarFileNameMediaServer").value = result.filename;
                formUserRegister.submit();
            }
            enableRegistrationButton();
        });
    } else if (allFieldsAreValidated) {
        formUserRegister.submit();
        enableRegistrationButton();
    } else {

    }
});
