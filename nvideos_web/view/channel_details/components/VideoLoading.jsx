import { useEffect, useState, useRef } from "react";
import { formatDuration, formatViews, formatDatetimeToString } from '../../base/entries/constants/utils';

import { ROUTES } from "../../base/entries/constants/routes";

export default function VideoLoading({ channelDetails }){
    const [page, setPage] = useState(0);
    const [videos, setVideos ] = useState([]);
    
    const divLoadingPoint = useRef(null);
    const hasMore = useRef(true);
    const isLoading = useRef(false);

    const loadMoreVideos = () => {
        if (!isLoading.current && hasMore.current){
            isLoading.current = true;

            fetch(ROUTES.channelVideoList(channelDetails?.channelId, page))
                .then((r) => r.json())
                .then((dataVideos) => {
                    if (dataVideos?.videos) {
                        setVideos((prev) => [...prev, ...dataVideos?.videos]);
                        setPage((prev) => prev + 1);
                    }
                    if (dataVideos?.videos?.length <= 0){
                        hasMore.current = false;
                    }
                    isLoading.current = false;
                });
        }
    };

    useEffect(()=>{
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && hasMore.current) {
                    loadMoreVideos();
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(divLoadingPoint.current);
        
        return () => {
            observer.disconnect();
        };
    }, [page]);
    
    return (
        <div className="contents">
            {videos.map((vd)=>
                <div key={vd?.videoId} className="flex flex-col gap-3.5 group cursor-pointer">
                    <div
                        className="aspect-video bg-surface rounded-2xl overflow-hidden border border-white/10 group-hover:border-brand/50 transition-all relative shadow-md">
                        <img src={vd?.videoThumbUrl}
                            className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                            alt="Video Thumbnail"/>
                        <div className="absolute bottom-2 right-2 bg-black/85 text-xs font-bold px-2 py-1 rounded text-white">
                            {formatDuration(vd?.videoTimeDuration)}</div>
                    </div>
                    <div className="flex gap-3">
                        <img src={channelDetails?.channelAvatarUrl}
                            className="w-10 h-10 rounded-full object-cover shrink-0 border border-brand/30"
                            alt="Channel Avatar"/>
                        <div className="flex-1 min-w-0">
                            <h4
                                className="font-bold text-sm text-white line-clamp-2 leading-snug group-hover:text-brand transition">
                                {vd?.videoTitle}
                            </h4>
                            <p className="text-xs text-gray-400 mt-1">{channelDetails?.channelName}</p>
                            <p className="text-xs text-gray-400 mt-0.5">{formatViews(vd?.videoViewCount)} • {formatDatetimeToString(vd?.createdAt)}</p>
                        </div>
                    </div>
                </div>
            )}
            <div ref={divLoadingPoint} className="w-full h-4"></div>
        </div>
    );
};