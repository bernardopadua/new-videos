import React from "react";
import ReactDOM from "react-dom/client";
import AvatarUploadUserDetails from "../components/AvatarUploadUserDetails";

const avatarUploadRoot = document.getElementById("avatar-upload-root");

if(avatarUploadRoot){
    ReactDOM.createRoot(avatarUploadRoot).render(
        <React.StrictMode>
            <AvatarUploadUserDetails />
        </React.StrictMode>
    );
}