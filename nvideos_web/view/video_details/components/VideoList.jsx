import { useState, useEffect } from 'react';
import { ROUTES } from '../../base/entries/constants/routes'

function VideoCard({ video }) {
    const [videoStatus, setVideoStatus] = useState(video?.videoStatus ?? "processed");

    const formatDuration = (seconds) => {
        if (!seconds) return "00:00";
        
        const hours = seconds > 3600 ? Math.floor(seconds / 3600) : '00';
        const minutes = seconds > 3600 ? Math.floor((seconds % 3600) / 60).toString().padStart(2, '0') : Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = Math.round(seconds % 60).toString().padStart(2, '0');

        return hours !== '00' ? `${hours}:${minutes}:${secs}` : `${minutes}:${secs}`;
    };

    useEffect(() => {
        let timer = null;
        let isMounted = true;
        const fetchForStatus = () => {
            fetch(ROUTES.videoGetStatusPercent(video.videoKey))
                .then((r) => r.json())
                .then((d) => {
                    if (d?.percent == 100) {
                        setVideoStatus("processed");
                    } else {
                        timer = setTimeout(() => {
                            fetchForStatus();
                        }, 2000);
                    }
                })
                .catch((e) => {
                    if (isMounted) {
                        console.log(e);
                    }
                });
        };

        if(video?.videoStatus === "processing") {
            fetchForStatus();
        }

        return () => { clearTimeout(timer); isMounted = false; }
    }, []);
    
    return (
        <div className="flex flex-col rounded-2xl bg-surface/90 border border-white/10 backdrop-blur-md overflow-hidden shadow-xl hover:border-white/20 transition-all duration-300 group">
            
            {/* THUMBNAIL CONTAINER */}
            <div className="relative aspect-video bg-[#121212] overflow-hidden">
                {video?.videoThumbUrl ?
                    (<img src={video?.videoThumbUrl} alt={video?.videoTitle}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />)
                : 
                    (<div className="w-full h-full flex flex-col items-center justify-center text-gray-600 gap-2">
                        <span className="text-4xl">🎬</span>
                        <span className="text-xs font-medium">Sem miniatura</span>
                    </div>)
                }
                {video?.videoTimeDuration ? (
                    <div className="absolute bottom-3 right-3 z-10 px-2 py-0.5 rounded bg-black/75 text-white text-xxs font-medium font-mono backdrop-blur-sm shadow-sm select-none">
                        {formatDuration(video.videoTimeDuration)}
                    </div>
                ) : null}
                {/* STATUS BADGE IN THUMBNAIL (ABSOLUTE) */}
                <div className="absolute top-3 right-3 z-10">
                    {videoStatus ?
                        videoStatus === "processed" ?
                            (<span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 backdrop-blur-sm shadow-sm">
                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                                Processado
                            </span>)
                        : videoStatus == "processing" ?
                            (<span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20 backdrop-blur-sm shadow-sm animate-pulse">
                                <span className="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
                                Processando...
                            </span>)
                        :
                            (<span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20 backdrop-blur-sm shadow-sm">
                                <span className="h-1.5 w-1.5 rounded-full bg-rose-400"></span>
                                Erro
                            </span>)
                        : null
                    }
                </div>
            </div>

            {/* CARD BODY */}
            <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                <div>
                    {/* TITLE */}
                    <h3 className="text-base font-bold text-white group-hover:text-brand transition-colors duration-200 line-clamp-1">
                        {video?.videoTitle}
                    </h3>
                    
                    {/* DESCRIPTION */}
                    <p className="text-xs text-gray-400 mt-2 line-clamp-2 leading-relaxed">
                        {video?.videoDescription}
                    </p>
                </div>

                {/* ACTIONS & DETAILS */}
                <div className="pt-4 border-t border-white/5 flex items-center justify-between gap-2">
                    <span className="text-xxs text-gray-500 font-mono tracking-wider uppercase">
                        KEY: {video.videoKey}
                    </span>
                    
                    <div className="flex items-center gap-2">
                        <a href={ROUTES.videoEdit(video.videoKey)}
                            className="px-3.5 py-1.5 text-xs font-semibold text-gray-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg transition duration-200"
                        >
                            Editar
                        </a>
                        {video?.videoStatus && video?.videoStatus === 'processed' ?
                            (<a href={ROUTES.videoDetail(video.videoKey)}
                                className="px-3.5 py-1.5 text-xs font-semibold text-white bg-white/10 hover:bg-white/20 border border-white/10 rounded-lg transition duration-200"
                            >
                                Assistir
                            </a>)
                        :
                            (<button disabled className="px-3.5 py-1.5 text-xs font-semibold text-gray-600 bg-white/5 border border-white/5 rounded-lg cursor-not-allowed" title="Aguarde o processamento concluir para assistir">
                                Assistir
                            </button>)
                        }
                    </div>
                </div>
            </div>

        </div>

    );
};

export default function VideoListing({ initialData }) {
    const [videos, setVideos] = useState(initialData?.videos ?? []);
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(initialData?.hasMore);

    const handleLoadMore = () => {
        fetch(ROUTES.videoSelfChannel(page + 1))
            .then((r) => r.json())
            .then((d) => {
                if (d && d?.videos && d?.videos.length > 0) {
                    setVideos([...videos, ...d?.videos]);
                    setPage(page + 1);
                    setHasMore(d?.hasMore);
                } else {
                    setHasMore(d?.hasMore);
                }
            })
            .catch((e) => {
                console.log(e);
            });
    };

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {videos && videos.map(video => (
                    <div key={video.videoId}>
                        <VideoCard video={video} />
                    </div>
                ))}
            </div>
            {hasMore ?
                (<div className="flex justify-center mt-8">
                    <button
                        className="p-3 rounded-xl bg-brand text-white hover:bg-[#772ce8] transition duration-200 shadow-lg shadow-brand/20 flex items-center justify-center"
                        ariaLabel="Load more"
                        onClick={handleLoadMore}
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                        </svg>
                    </button>
                </div>) : null
            }
        </div>
    );
}