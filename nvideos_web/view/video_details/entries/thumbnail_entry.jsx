import React from 'react';
import ReactDom from 'react-dom/client';
import ThumbnailUpload from '../components/ThumbnailUpload';

const root = ReactDom.createRoot(document.getElementById("thumbnail-root"));
root.render(
    <React.StrictMode>
        <ThumbnailUpload />
    </React.StrictMode>
);