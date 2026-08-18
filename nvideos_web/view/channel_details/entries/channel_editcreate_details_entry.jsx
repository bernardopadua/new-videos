import React from 'react';
import ReactDOM from 'react-dom/client';

import BannerChannel from '../components/BannerChannel';
import AvatarUpload from '../components/AvatarUpload';

import ChannelImageUpload from './channel_image_upload/channel_image_upload_editcreate';

const formChannel = document.getElementById("channel-details-form");
formChannel.addEventListener("submit", (e) => {
    e.preventDefault();

    const mediaUpload = new ChannelImageUpload();
    const submitFormCallback = () => {
        formChannel.submit();
    }

    mediaUpload.doUploadMedia(submitFormCallback);
});

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
