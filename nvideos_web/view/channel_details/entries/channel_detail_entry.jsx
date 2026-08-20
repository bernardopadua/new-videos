import ReactDOM from 'react-dom/client';

import VideoLoading from '../components/VideoLoading';
import CheckChannelSubscription from '../../subscriber/entries/channel_subscription/check_channel_subscription';

//Checkfor subscription
CheckChannelSubscription();

const videoLoadingRoot = document.getElementById("video-loading-root");
const channelDetailsJson = document.getElementById("channel-details-json").textContent;
const channelDetails = JSON.parse(channelDetailsJson);
if (videoLoadingRoot){
    ReactDOM.createRoot(videoLoadingRoot).render(
        <VideoLoading channelDetails={channelDetails}/>
    );
}