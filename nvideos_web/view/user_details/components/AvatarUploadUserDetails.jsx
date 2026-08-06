import { useState } from "react";

export default function AvatarUploadUserDetails({ userAvatarUrlValue, userAvatarUrl }) {
    const [imagePreview, setImagePreview] = useState(userAvatarUrlValue);

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
                userAvatarUrl.setAttribute('changed', true);
                userAvatarUrl.value = "";
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div class="p-8 sm:p-10 rounded-3xl bg-surface/90 border border-white/10 backdrop-blur-md flex flex-col sm:flex-row items-center gap-8 shadow-xl">
            <label for="userAvatar" class="relative group cursor-pointer shrink-0">
                <input id="userAvatar" name="userAvatar" type="file" accept="image/*" class="sr-only" onChange={handleImageChange} />

                <div class="w-36 h-36 rounded-full bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 shadow-inner relative">
                    {imagePreview ?
                        (<img id="userAvatarPreview" class="w-full h-full object-cover rounded-full" alt="Avatar Preview"
                            src={imagePreview}
                        />)
                    :
                    (<div id="userAvatarPlaceholder" class="flex flex-col items-center justify-center p-3 text-center transition-transform duration-200 group-hover:scale-105">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span class="text-xs font-semibold text-gray-200 mt-2 group-hover:text-white">Upload Avatar</span>
                    </div>)
                    }
                </div>

                <div class="absolute bottom-1 right-1 bg-brand text-white p-2.5 rounded-full shadow-lg border-2 border-bg-dark transition-transform duration-200 group-hover:scale-110">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                </div>
            </label>

            <div class="space-y-2 text-center sm:text-left">
                <h3 class="text-xl font-bold text-white">Profile Photo</h3>
                <p class="text-xs sm:text-sm text-gray-400">Click on the image circle to upload a new profile picture.</p>
                <span class="text-xs text-gray-500 block pt-1">Recommended size: 400x400 (PNG, JPG or WEBP).</span>
            </div>
        </div>
    );
};