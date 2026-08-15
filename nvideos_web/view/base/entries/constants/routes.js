export const ROUTES = {
    //Subscriber
    isSubscribedChannel: (channelId) => `/channel/${channelId}/subscribed`,
    subscribeChannel: (channelId) => `/channel/${channelId}/subscribe`,
    unsubscribeChannel: (channelId) => `/channel/${channelId}/unsubscribe`,
    totalSubscribedChannel: (channelId) => `/channel/${channelId}/total-subscribers`,
    
    //Comment
    loadReplies: (commentId) => `/comment/load/replies/${commentId}`,
    commentReply: (videoId, commentId = null) => {
        if (commentId){
            return `/comment/reply/${videoId}/${commentId}`;
        } else {
            return `/comment/reply/${videoId}`;
        }
    },

    //Video
    videoEdit: (videoKey) => `/video/${videoKey}/edit`,
    videoDetail: (videoKey) => `/video/${videoKey}`,
    videoSelfChannel: (page) => `/video/list/paging/${page}`,
    videoGetStatusPercent: (videoKey) => `/video/status/${videoKey}`,

    videoWatchMediaServer: (videoKey) => `/video/${videoKey}/playlist.m3u8`,
};