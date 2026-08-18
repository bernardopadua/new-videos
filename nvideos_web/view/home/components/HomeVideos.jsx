import { useState, useEffect, useRef } from "react";
import { ROUTES } from "../../base/entries/constants/routes";
import { formatDuration, formatViews } from '../../base/entries/constants/utils';

function VideoCard({ video }) {
    const videoTimeDuration = formatDuration(video?.videoTimeDuration);
    const videoTitle = video?.videoTitle;
    const videoKey = video?.videoKey;
    const videoThumbUrl = video?.videoThumbUrl;
    const videoChannelName = video?.channelName;
    const videoChannelAvatar = video?.channelAvatarUrl;
    const videoViews = formatViews(video?.videoViewCount);
    
    return (
        <a href={ROUTES.videoDetail(videoKey)} className="group bg-surface/40 hover:bg-surface/80 border border-white/5 hover:border-brand/40 rounded-2xl p-3.5 transition-all duration-300 hover:-translate-y-1 shadow-lg flex flex-col justify-between gap-3">
            <div className="aspect-video bg-black rounded-xl overflow-hidden relative border border-white/5">
                <img src={videoThumbUrl} className="w-full h-full object-cover group-hover:scale-105 transition duration-500" alt="Thumbnail" />
                <span className="absolute bottom-2.5 right-2.5 bg-black/85 backdrop-blur-md text-[11px] font-bold px-2 py-0.5 rounded text-white border border-white/10">{videoTimeDuration}</span>
            </div>
            <div className="flex gap-3 items-start">
                <img src={videoChannelAvatar} className="w-10 h-10 rounded-full border border-brand/50 object-cover shrink-0 mt-0.5" alt="Avatar" />
                <div className="space-y-1 min-w-0">
                    <h3 className="font-bold text-sm text-white group-hover:text-brand line-clamp-2 leading-snug transition">
                        {videoTitle}
                    </h3>
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                        <span className="hover:text-gray-200">{videoChannelName}</span>
                            <svg className="w-3.5 h-3.5 text-brand fill-current"
                                viewBox="0 0 20 20"
                            >
                                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
                            </svg>
                    </div>
                    <p className="text-xs text-gray-400">{videoViews}</p>
                </div>
            </div>
        </a>
    );
};

export default function HomeVideos() {
    const [filter, setFilter] = useState('recent');
    const [page, setPage] = useState(0);
    const [videos, setVideos] = useState([]);
    const loaderRef = useRef(null);
    const hasMoreRef = useRef(false);

    const handleFilterChange = (newFilter) => {
        setPage(0);
        setFilter(newFilter);
    };

    const filterSelected = "text-brand font-bold cursor-pointer";
    const filterToSelect = "hover:text-white cursor-pointer transition";

    useEffect(() => {
        let ignore = false;

        const getVideosByFilter = () => {
            fetch(ROUTES.videosHome(page, filter))
                .then(res => res.json())
                .then((data) => {
                    if (!ignore){
                        setVideos((prev) => { return [...prev, ...data?.videos] });
                        hasMoreRef.current = data?.hasMore;
                    }
                });
        };

        getVideosByFilter();

        return () => { ignore = true; };
    }, [page, filter]);

    useEffect(() => {
        const ob = new IntersectionObserver(
            (e) => {
                if (e && e[0].isIntersecting && hasMoreRef.current) {
                    setPage(p => p + 1);
                    hasMoreRef.current = false;
                }
            }
        );
        ob.observe(loaderRef.current);

        return () => { ob.disconnect(); }
    }, []);

    return (
        <div id="videos-home" className="w-full">
            <div className="max-w-[1700px] mx-auto space-y-8 sm:space-y-10 pb-20">

                <div className="flex items-center justify-between pt-4">
                    <div className="flex items-center gap-2 text-xs font-semibold text-gray-400">
                        <span className={filter == 'recent' ? filterSelected : filterToSelect}
                            onClick={filter != 'recent' ? () => handleFilterChange('recent') : null}
                        >
                            Recent
                        </span>
                        {/*<span>•</span>
                        <span className="text-brand font-bold cursor-pointer"
                            onClick={() => handleFilterChange('trending')}
                        >
                            Trending
                        </span>
                        
                        //I don't have enough "data" to calibrate what is "trending".
                        //Maybe in the future.
                        */}
                        <span>•</span>
                        <span className={filter == 'most-viewed' ? filterSelected : filterToSelect}
                            onClick={filter != 'most-viewed' ? () => handleFilterChange('most-viewed') : null}
                        >
                            Most Viewed
                        </span>
                    </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {videos.length <= 0 ?
                        (<div className="col-span-full py-20 flex flex-col items-center justify-center border border-dashed border-white/10 rounded-2xl bg-surface/20 text-center gap-2">
                            <svg className="w-10 h-10 text-gray-500/80" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                            </svg>
                            <p className="text-sm font-medium text-gray-400">No videos</p>
                        </div>)
                    :
                        videos.map((video) => (
                            <VideoCard key={video.videoId} video={video} />
                        ))
                    }
                </div>

            </div>
        
            <div ref={loaderRef} className="h-10 w-full flex items-center justify-center">
                
            </div>
            
        </div>
    );
};