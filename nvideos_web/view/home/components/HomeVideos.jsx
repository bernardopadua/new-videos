import { useState } from "react";

function VideoCard() {
    return (
        <a href="/player" className="group bg-surface/40 hover:bg-surface/80 border border-white/5 hover:border-brand/40 rounded-2xl p-3.5 transition-all duration-300 hover:-translate-y-1 shadow-lg flex flex-col justify-between gap-3">
            <div className="aspect-video bg-black rounded-xl overflow-hidden relative border border-white/5">
                <img src="https://picsum.photos/600/338?random=1" className="w-full h-full object-cover group-hover:scale-105 transition duration-500" alt="Thumbnail" />
                <span className="absolute bottom-2.5 right-2.5 bg-black/85 backdrop-blur-md text-[11px] font-bold px-2 py-0.5 rounded text-white border border-white/10">14:20</span>
                <span className="absolute top-2.5 left-2.5 bg-brand/90 text-white text-[10px] font-extrabold px-2 py-0.5 rounded uppercase">Dev</span>
            </div>
            <div className="flex gap-3 items-start">
                <img src="https://picsum.photos/80/80?random=12" className="w-10 h-10 rounded-full border border-brand/50 object-cover shrink-0 mt-0.5" alt="Avatar" />
                <div className="space-y-1 min-w-0">
                    <h3 className="font-bold text-sm text-white group-hover:text-brand line-clamp-2 leading-snug transition">
                        Como criar um clone do YouTube com Tailwind v4 e Flask
                    </h3>
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                        <span className="hover:text-gray-200">DevPro Studio</span>
                            <svg className="w-3.5 h-3.5 text-brand fill-current"
                                viewBox="0 0 20 20"
                            >
                                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
                            </svg>
                    </div>
                    <p className="text-xs text-gray-400">1.2M views • há 3 horas</p>
                </div>
            </div>
        </a>
    );
};

export default function HomeVideos() {
    const [filter, setFilter] = useState('recentes');

    const handleFilterChange = (newFilter) => {
        setFilter(newFilter);
    };

    return (

        <div className="max-w-[1700px] mx-auto space-y-8 sm:space-y-10 pb-20">

            <div className="flex items-center justify-between pt-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-gray-400">
                    <span className="hover:text-white cursor-pointer transition"
                        onClick={() => handleFilterChange('recent')}
                    >
                        Recent
                    </span>
                    <span>•</span>
                    <span className="text-brand font-bold cursor-pointer"
                        onClick={() => handleFilterChange('trending')}
                    >
                        Trending
                    </span>
                    <span>•</span>
                    <span className="hover:text-white cursor-pointer transition"
                        onClick={() => handleFilterChange('most-viewed')}
                    >
                        Most Viewed
                    </span>
                </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                
                <div className="col-span-full py-20 flex flex-col items-center justify-center border border-dashed border-white/10 rounded-2xl bg-surface/20 text-center gap-2">
                    <svg className="w-10 h-10 text-gray-500/80" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
                    </svg>
                    <p className="text-sm font-medium text-gray-400">No videos</p>
                </div>

            </div>

        </div>

    );
};