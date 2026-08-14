import React from 'react';
import ReactDOM from 'react-dom/client';

import VideoPlayerInit from "./video_player/video_player";
import VideoDescriptionToggle from "./video_detail/video_description_toggle";
import VideoSubscribe from "./video_detail/video_subscribe";

import VideoComments from "../components/VideoComments";

//Init video player
VideoPlayerInit();

//VideoDescription Toggle
VideoDescriptionToggle();

//VideoSubscribe button
VideoSubscribe();

const commentsSectionRoot = document.getElementById('comments-section-root');
if (commentsSectionRoot) {
    const initialComments = JSON.parse(document.getElementById('initial-comment-data').textContent);
    ReactDOM.createRoot(commentsSectionRoot).render(
        <React.StrictMode>
            <VideoComments initialComments={initialComments} />
        </React.StrictMode>
    );
}
