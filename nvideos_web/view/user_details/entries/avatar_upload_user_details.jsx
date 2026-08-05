import React from "react";
import ReactDOM from "react-dom/client";
import AvatarUploadUserDetails from "../components/AvatarUploadUserDetails";

const avatarUploadRoot = document.getElementById("avatar-upload-root");
const userAvatarUrl = document.getElementById("avatarFileNameMediaServer");

if(avatarUploadRoot){
    ReactDOM.createRoot(avatarUploadRoot).render(
        <React.StrictMode>
            <AvatarUploadUserDetails
                userAvatarUrlValue={userAvatarUrl.value}
                userAvatarUrl={userAvatarUrl}
            />
        </React.StrictMode>
    );
}