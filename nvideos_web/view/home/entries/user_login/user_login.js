class UserLogin {
    constructor() {
        this._userEmail = document.getElementById("userEmail");
        this._userPassword = document.getElementById("userPassword");
    }

    _validateAllFields() {
        const validUserEmail = this._validateUserEmail();
        const validUserPassword = this._validateUserPassword();
        document.getElementById('login-error-alert').classList.add('hidden');
        
        if (validUserEmail && validUserPassword) {
            return true;
        }

        document.getElementById('login-error-alert').classList.remove('hidden');
        return false;
    }

    _validateUserEmail() {
        const userEmail = this._userEmail.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (userEmail.length === 0) {
            document.getElementById("login-warning-empty-email").classList.remove("hidden");
            return false;
        }

        if (!emailRegex.test(userEmail)) {
            document.getElementById('login-warning-invalid-email').classList.remove('hidden');
            return false;
        }

        return true;
    }

    _validateUserPassword() {
        const userPassword = this._userPassword.value;
        if (userPassword.length === 0) {
            document.getElementById('login-warning-empty-password').classList.remove('hidden');
            return false;
        }

        return true;
    }

    _resetBulletAlert() {
        document.querySelectorAll(".error-text").forEach((bulletAlert) => {
            bulletAlert.classList.add("hidden");
        });
    }
}

const formLogin = document.getElementById("login-form");
formLogin.addEventListener("submit", (event) => {

    const usuLogin = new UserLogin();
    usuLogin._resetBulletAlert();

    if (!usuLogin._validateAllFields()) {
        event.preventDefault();
    }
});