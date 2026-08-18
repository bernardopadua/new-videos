import { useState } from "react";

export default function AvatarUpload({ avatarFileNameMediaServer }) {
    const [avatarPreview, setAvatarPreview] = useState(avatarFileNameMediaServer.value);
    
    const handleChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setAvatarPreview(URL.createObjectURL(file));
        }
    };

    return (
        <div className="pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center gap-6">
            <label htmlFor="channelAvatarFile" className="relative group cursor-pointer shrink-0">
                <input
                    id="channelAvatarFile"
                    name="channelAvatarFile"
                    type="file" accept="image/*"
                    className="sr-only"
                    onChange={handleChange}
                />

                <div className="w-32 h-32 rounded-full bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 shadow-inner relative">
                    {avatarPreview ?
                        <img id="channelAvatarPreview" src={avatarPreview} className="w-full h-full object-cover rounded-full" alt="Channel Avatar Preview" />
                    :
                        <div id="channelAvatarPlaceholder" className="flex flex-col items-center justify-center p-2 text-center transition-transform duration-200 group-hover:scale-105">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span className="text-xs font-semibold text-gray-300 mt-1 group-hover:text-white">Channel Avatar</span>
                        </div>
                    }
                </div>

                <div className="absolute bottom-1 right-1 bg-brand text-white p-2 rounded-full shadow-lg border-2 border-bg-dark">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                    </svg>
                </div>
            </label>

            <div className="space-y-1.5 text-center sm:text-left">
                <h4 className="text-base font-bold text-white">Channel Profile Picture</h4>
                <p className="text-xs sm:text-sm text-gray-400">This avatar represents your channel next to your videos and comments.</p>
            </div>
        </div>
    );
}