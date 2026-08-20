import React from 'react';
import ReactDOM from 'react-dom/client';

import BannerChannel from '../components/BannerChannel';
import AvatarUpload from '../components/AvatarUpload';

import ChannelImageUpload from './channel_image_upload/channel_image_upload_editcreate';
import ChannelEditDetailsValidation from './channel_details_edit/channel_details_edit';

const bannerCoverUrl = document.getElementById("bannerCoverImageUrl");
const rootCoverImage = ReactDOM.createRoot(document.getElementById("root-cover-image"));
rootCoverImage.render(
    <React.StrictMode>
        <BannerChannel bannerCoverUrl={bannerCoverUrl} />
    </React.StrictMode>
);

const avatarFileNameMediaServer = document.getElementById("avatarFileNameMediaServer");
const rootAvatar = ReactDOM.createRoot(document.getElementById("root-avatar"));
rootAvatar.render(
    <React.StrictMode>
        <AvatarUpload avatarFileNameMediaServer={avatarFileNameMediaServer} />
    </React.StrictMode>
);

const formChannel = document.getElementById("channel-details-form");
formChannel.addEventListener("submit", (e) => {
    e.preventDefault();

    const fieldValidation = new ChannelEditDetailsValidation();
    const validFields = fieldValidation.validateAllFields();

    console.log(validFields);
    if (validFields) {
        const mediaUpload = new ChannelImageUpload();
        const submitFormCallback = () => {
            formChannel.submit();
        }

        mediaUpload.doUploadMedia(submitFormCallback);
    }
});