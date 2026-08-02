import { useState } from 'react';

export default function AvatarUpload() {
  const [preview, setPreview] = useState(null)

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const imageUrl = URL.createObjectURL(file)
      setPreview(imageUrl)
    }
  }

  return (
    <div class="flex flex-col items-center justify-center space-y-3">
      <span class="block text-xs font-semibold text-gray-300 uppercase tracking-wider">
        Profile Picture
      </span>

      <label htmlFor="userAvatar" class="relative group cursor-pointer flex flex-col items-center">
        <input 
          id="userAvatar" 
          name="userAvatar" 
          type="file" 
          accept="image/*" 
          class="sr-only" 
          onChange={handleImageChange} 
        />

        <div class="w-32 h-32 rounded-full bg-[#121212] border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden transition-all duration-300 group-hover:border-brand group-hover:ring-4 group-hover:ring-brand/20 shadow-inner relative">
          {preview ? (
            <img src={preview} class="w-full h-full object-cover rounded-full" alt="Avatar Preview" />
          ) : (
            <div class="flex flex-col items-center justify-center p-2 text-center transition-transform duration-200 group-hover:scale-105">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 group-hover:text-brand transition duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="text-xs font-medium text-gray-300 mt-1.5 group-hover:text-white">Upload Photo</span>
              <span class="text-[10px] text-gray-500">PNG, JPG or WEBP</span>
            </div>
          )}
        </div>

        <div class="absolute bottom-0 right-0 bg-brand text-white p-2 rounded-full shadow-lg border-2 border-bg-dark transition-transform duration-200 group-hover:scale-110">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
          </svg>
        </div>
      </label>
    </div>
  )
};
