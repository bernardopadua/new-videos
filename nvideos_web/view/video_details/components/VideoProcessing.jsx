import { useState, useEffect } from "react";

export default function VideoProcessing({ videoKeyInput, videoStatusInput, videoThumbUrlInput }) {
    const [videoStatus, setVideoStatus] = useState(videoStatusInput?.value);
    const [processingPercent, setProcessingPercent] = useState("0%");

    const videoKey = videoKeyInput?.value;
    const videoThumbUrl = videoThumbUrlInput?.value;

    useEffect(() => {
        let timer;
        let isMounted = true;

        const fetchVideoStatus = async () => {
            try {
                const response = await fetch(`/video/status/${videoKey}`);
                if (response.ok) {
                    const data = await response.json();

                    if (parseInt(data?.percent) < 100) {
                        setProcessingPercent(`${data.percent}%`);
                        timer = setTimeout(() => {
                            fetchVideoStatus();
                        }, 1500);
                    } else if (parseInt(data?.percent) == 100) {
                        clearTimeout(timer);
                        setVideoStatus('processed');
                        setProcessingPercent('100%');

                        //Signal to other components that the video processing has finished.
                        window.dispatchEvent(new CustomEvent('video-processing-finished'));
                    } else if (data?.percent == null) {
                        timer = setTimeout(() => {
                            fetchVideoStatus();
                        }, 5000);
                    } else {
                        clearTimeout(timer);
                        console.error("Error fetching video status");
                    }
                }
            } catch (error) {
                if (isMounted)
                    console.error("Error fetching video status:", error);
            }
        };

        if (videoStatus == 'processing') {
            fetchVideoStatus();
        }

        return () => { isMounted = false; clearTimeout(timer); }
    }, []);

    return (
        <div className="p-8 sm:p-10 rounded-3xl bg-surface/90 border border-white/10 backdrop-blur-md space-y-6 shadow-xl">
            <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>🎥</span> Video Status
                </h3>
                <p className="text-xs sm:text-sm text-gray-400 mt-1">Status of video processing and media delivery.</p>
            </div>

            <div className="flex flex-col md:flex-row gap-6 items-start md:items-center">
                {/*Thumbnail Container*/}
                <div className="relative w-full md:w-64 aspect-video rounded-2xl overflow-hidden bg-black/40 border border-white/10 shadow-inner group">
                    <img src={videoThumbUrl} alt="Video thumbnail" className="w-full h-full object-cover" />

                    {/*Processing Overlay (Visible when processing)*/}
                    {videoStatus == 'processing' ?
                        (<div className="absolute inset-0 bg-black/60 flex items-center justify-center backdrop-blur-sm transition-all duration-300">
                            <div className="flex flex-col items-center gap-2">
                                <svg className="animate-spin h-8 w-8 text-brand" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <span className="text-xs font-semibold text-brand tracking-wider uppercase">Processing</span>
                            </div>
                        </div>) : null
                    }
                </div>

                {/*Info Side*/}
                <div className="flex-1 w-full space-y-4">
                    {videoStatus == 'processing' ?
                        /*Processing Info and Progress Bar*/
                        (<div className="space-y-3">
                            <div className="flex items-center gap-2 text-amber-400 font-semibold text-sm">
                                <span className="relative flex h-2.5 w-2.5">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
                                </span>
                                <span>Transcoding and processing video...</span>
                            </div>
                            <p className="text-xs text-gray-400">We are processing and preparing your video for smooth streaming. This might take a few minutes.</p>

                            {/*Progress Bar*/}
                            <div className="w-full mt-4 space-y-2">
                                <div className="flex justify-between text-xs text-gray-400 font-semibold">
                                    <span>Processing...</span>
                                    <span id="video-processing-percent">{processingPercent}</span>
                                </div>
                                <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                                    <div id="video-processing-bar" className="bg-brand h-full transition-all duration-300 rounded-full" style={{ width: processingPercent }}></div>
                                </div>
                            </div>
                        </div>)
                        :
                        /*Processed Info*/
                        (<div className="space-y-2">
                            <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
                                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span>Ready to watch</span>
                            </div>
                            <p className="text-xs text-gray-400">The video has been successfully processed and is ready for public streaming.</p>
                        </div>)
                    }
                </div>
            </div>
        </div>
    );
}