import React from 'react';
import ReactDOM from 'react-dom/client';

import VideoPlayerInit from "./video_player/video_player";
import VideoDescriptionToggle from "./video_detail/video_description_toggle";
import CheckChannelSubscription from "../../subscriber/entries/channel_subscription/check_channel_subscription";

import VideoComments from "../components/VideoComments";

//Init video player
VideoPlayerInit();

//VideoDescription Toggle
VideoDescriptionToggle();

//VideoSubscribe button
CheckChannelSubscription();

const commentsSectionRoot = document.getElementById('comments-section-root');
if (commentsSectionRoot) {
    const initialComments = JSON.parse(document.getElementById('initial-comment-data').textContent);
    const initialData = JSON.parse(document.getElementById('initial-data').textContent);
    ReactDOM.createRoot(commentsSectionRoot).render(
        <React.StrictMode>
            <VideoComments initialComments={initialComments} initialData={initialData} />
        </React.StrictMode>
    );
}
