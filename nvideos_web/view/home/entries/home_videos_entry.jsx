import HomeVideos from '../components/HomeVideos';
import React from 'react';
import ReactDOM from 'react-dom/client';

const homeVideosRoot = document.getElementById("home-videos-root");
if (homeVideosRoot) {
    ReactDOM.createRoot(homeVideosRoot).render(
        <React.StrictMode>
            <HomeVideos />
        </React.StrictMode>
    )
}