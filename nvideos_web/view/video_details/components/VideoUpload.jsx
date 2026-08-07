import { useState } from 'react';

export default function VideoUpload() {
    const [videoLoaded, setVideoLoaded] = useState(false);
    const [nameSpan, setNameSpan] = useState("");
    const [sizeSpan, setSizeSpan] = useState("");

    const handleChange = (e) => {
        setVideoLoaded(false);
        const file = e.target.files[0];

        if (file) {
            const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);

            setNameSpan(file.name);
            setSizeSpan(`${sizeInMB} MB`);
            setVideoLoaded(true);
        }
    };
    
    return (
        <div class="p-8 sm:p-10 rounded-3xl bg-surface/90 border border-white/10 backdrop-blur-md space-y-6 shadow-xl">
            <div>
                <h3 class="text-lg font-bold text-white flex items-center gap-2">
                    <span>🎥</span> Video File
                </h3>
                <p class="text-xs sm:text-sm text-gray-400 mt-1">Select the video file you want to upload (.mp4, .mkv, .mov, etc.).</p>
            </div>
            
            <label for="video_file" class="relative group cursor-pointer block">
                <input id="video_file" name="video_file" type="file" accept="video/*" class="sr-only"
                    onChange={handleChange}
                />
                
                    <div class="w-full rounded-2xl bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center p-8 transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 relative shadow-inner">
                    {!videoLoaded ?
                        (<div id="videoPlaceholder" class="flex flex-col items-center justify-center p-6 text-center group-hover:scale-105 transition duration-200">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            <span class="text-sm font-semibold text-gray-200 mt-3 group-hover:text-white">Choose Video File</span>
                            <span class="text-xs text-gray-500 mt-1">MP4, MKV, AVI, MOV or WEBM</span>
                        </div>)
                        :
                        (<div id="videoInfo" class="flex flex-col items-center justify-center p-6 text-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-brand" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span class="text-sm font-semibold text-gray-200 mt-3 break-all">{nameSpan}</span>
                            <span class="text-xs text-gray-500 mt-1 text-center">{sizeSpan}</span>
                        </div>)
                    }
                    </div>
            </label>
        </div>
    );
};