import React from "react";
import ReacDOM from "react-dom/client";
import VideoListing from "../components/VideoList";

const videoListingRoot = document.getElementById("video-listing-root");
const initialState = document.getElementById("initial-data");
if (videoListingRoot && initialState) {
    const initialData = JSON.parse(initialState.innerText);
    ReacDOM.createRoot(videoListingRoot).render(
        <React.StrictMode>
            <VideoListing initialData={initialData} />
        </React.StrictMode>
    );
}