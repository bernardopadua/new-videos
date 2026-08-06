import { useState } from "react";

export default function BannerChannel({ bannerCoverUrl }) {    
    const [bannerPreview, setBannerPreview] = useState(bannerCoverUrl.value);
    
    const handleChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setBannerPreview(URL.createObjectURL(file));
        }
    };

    return (
        <div class="space-y-3">
            <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider">Channel Banner Image</label>
            
            <label for="channelBannerFile" class="relative group cursor-pointer block">
                <input
                    id="channelBannerFile"
                    name="channelBannerFile"
                    type="file"
                    accept="image/*"
                    class="sr-only"
                    onChange={handleChange}
                />

                <div class="w-full h-44 sm:h-52 rounded-2xl bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 relative shadow-inner">
                    {bannerPreview ?
                        <img id="bannerPreview" src={bannerPreview} class="w-full h-full object-cover rounded-2xl" alt="Banner Preview" />
                        :
                        <div id="bannerPlaceholder" class="flex flex-col items-center justify-center p-4 text-center group-hover:scale-105 transition duration-200">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span class="text-xs font-semibold text-gray-200 mt-2 group-hover:text-white">Upload Banner Image</span>
                            <span class="text-[11px] text-gray-500 mt-1">Recommended: 2048 x 576 (PNG, JPG or WEBP)</span>
                        </div>
                    }
                </div>
            </label>
        </div>
    );
}