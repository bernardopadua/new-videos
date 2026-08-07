import React from 'react';
import ReactDom from 'react-dom/client';
import ThumbnailUpload from '../components/ThumbnailUpload';
import VideoUpload from '../components/VideoUpload';

import { videoUploadService } from './video_details_registration_editing';

const thumbnailRoot = ReactDom.createRoot(document.getElementById("thumbnail-root"));
thumbnailRoot.render(
    <React.StrictMode>
        <ThumbnailUpload />
    </React.StrictMode>
);

const videoRoot = ReactDom.createRoot(document.getElementById("video-root"));
videoRoot.render(
    <React.StrictMode>
        <VideoUpload videoUploadService={videoUploadService} />
    </React.StrictMode>
);