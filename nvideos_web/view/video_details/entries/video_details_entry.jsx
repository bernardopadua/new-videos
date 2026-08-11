import React from 'react';
import ReactDom from 'react-dom/client';
import ThumbnailUpload from '../components/ThumbnailUpload';
import VideoUpload from '../components/VideoUpload';
import VideoProcessing from '../components/VideoProcessing';

import { videoUploadService } from './video_details_registration_editing';

const thumbnailRoot = document.getElementById("thumbnail-root"); 
const thumbnailTempFilenameInput = document.getElementById("videoThumbTempFilename");
if (thumbnailRoot && thumbnailTempFilenameInput) {
    ReactDom.createRoot(thumbnailRoot).render(
        <React.StrictMode>
            <ThumbnailUpload thumbnailTempFilenameInput={thumbnailTempFilenameInput}  />
        </React.StrictMode>
    );
}
    
const videoRoot = document.getElementById("video-root");
if (videoRoot) {
    ReactDom.createRoot(videoRoot).render(
        <React.StrictMode>
            <VideoUpload videoUploadService={videoUploadService} />
        </React.StrictMode>
    );
}

const videoStatusInput = document.getElementById("videoStatusInput");
const videoThumbUrlInput = document.getElementById("videoThumbUrlInput");
const videoKeyInput = document.getElementById("videoKeyInput");

const videoProcessingRoot = document.getElementById("video-processing-root");
if (videoProcessingRoot) {
    ReactDom.createRoot(videoProcessingRoot).render(
        <React.StrictMode>
            <VideoProcessing videoStatusInput={videoStatusInput} videoThumbUrlInput={videoThumbUrlInput} videoKeyInput={videoKeyInput} />
        </React.StrictMode>
    );
}