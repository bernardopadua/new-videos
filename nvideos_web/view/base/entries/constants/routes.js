export const ROUTES = {
    //Video
    videoEdit: (videoKey) => `/video/${videoKey}/edit`,
    videoDetail: (videoKey) => `/video/${videoKey}`,
    videoSelfChannel: (page) => `/video/list/paging/${page}`,
    videoGetStatusPercent: (videoKey) => `/video/status/${videoKey}`,

    videoWatchMediaServer: (videoKey) => `/video/${videoKey}/playlist.m3u8`,
};