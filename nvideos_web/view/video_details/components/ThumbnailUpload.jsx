import { useState } from "react";

export default function ThumbnailUpload() {
    const [thumbImagePreview, setThumbImagePreview] = useState("");

    const handleChange = (e) => {
        const file = e.target.files[0];
        setThumbImagePreview(file ? URL.createObjectURL(file) : "");
    };

    return (
        <div class="p-8 sm:p-10 rounded-3xl bg-surface/90 border border-white/10 backdrop-blur-md space-y-6 shadow-xl">
            <div>
                <h3 class="text-lg font-bold text-white flex items-center gap-2">
                    <span>🖼️</span> Video Thumbnail
                </h3>
                <p class="text-xs sm:text-sm text-gray-400 mt-1">Upload a high-quality thumbnail image (16:9 ratio, recommended 1280x720).</p>
            </div>
            
            <label for="video_thumb_file" class="relative group cursor-pointer block">
                <input id="video_thumb_file" name="video_thumb_file" type="file" accept="image/*" class="sr-only"
                    onChange={handleChange}
                />
                
                <div class="w-full aspect-video sm:w-[440px] rounded-2xl bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 relative shadow-inner">
                    {thumbImagePreview ? (
                        <img src={thumbImagePreview} alt="Thumbnail Preview" className="w-full h-full object-cover rounded-2xl" />
                    ) : (
                        <div className="flex flex-col items-center justify-center p-6 text-center group-hover:scale-105 transition duration-200">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span class="text-sm font-semibold text-gray-200 mt-3 group-hover:text-white">Upload New Thumbnail</span>
                            <span class="text-xs text-gray-500 mt-1">PNG, JPG or WEBP (1280 x 720)</span>
                        </div>
                    )}
                </div>
            </label>
        </div>
    );
};