import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import obfuscator from 'rollup-plugin-obfuscator';
import fs from 'node:fs';

const cleanSomeDirs = () => ({
    name: 'clean-some-dirs',
    buildStart: () => {
        const dirs = [
            'base/static/dist'
        ];
        dirs.forEach((dir) => {
            fs.readdir(dir, (err, files) => {
                files.forEach((file) => {
                    fs.rmSync(dir + '/' + file);
                });
            });
        });
    }
});

export default defineConfig({
    plugins: [
        tailwindcss(),
        react(),
        cleanSomeDirs()
    ],
    build: {
        sourcemap: true,
        outDir: '.',
        emptyOutDir: false,
            rollupOptions: {
            plugins: [
                process.env.NODE_ENV === "production" ? obfuscator({
                    include: [
                        //Home
                        './home/entries/user_registration/user_register_form_validation.js'
                    ],
                    compact: true,
                    controlFlowFlattening: true,
                }) : null
            ],
            input: {
                //Base
                'base/main': './base/css/main.css',
                
                //Home
                'home/avatar_entry': './home/entries/avatar_entry.jsx',
                'home/user_register_form_validation/ufrv': './home/entries/user_registration/user_register_form_validation.js',
                'home/user_login/login': './home/entries/user_login/user_login.js',

                //UserDetails
                'user_details/avatar_upload_user_details/ausd': './user_details/entries/avatar_upload_user_details.jsx',
                'user_details/user_edit_details/ued': './user_details/entries/user_edit_details/user_edit_details.js',

                //ChannelDetails
                'channel_details/channel_editcreate_details/ced': './channel_details/entries/channel_editcreate_details_entry.jsx',
                'channel_details/channel_image_upload_editcreate/ciec': './channel_details/entries/channel_image_upload_editcreate.js',

                //VideoDetails
                'video_details/video_details_entry/vde': './video_details/entries/video_details_entry.jsx',
                'video_details/video_details_registration_editing/vdre': './video_details/entries/video_details_registration_editing.js',
                'video_details/video_listing_entry/vle': './video_details/entries/video_listing_entry.jsx',
                'video_details/video_player/vpl': './video_details/entries/video_player.js',
            },
            output: {
                entryFileNames: (chunkInfo) => {
                    const chunkName = chunkInfo.name.split('/');
                    if (chunkName.length == 3) {
                        const [module, name, subName] = chunkInfo.name.split('/');
                        return `${module}/static/dist/${subName}.js`;
                    }
                    const [module, name] = chunkInfo.name.split('/');
                    return `${module}/static/dist/${name}.js`;
                },
                chunkFileNames: (chunkInfo) => {
                    const name = chunkInfo.name;
                    return `base/static/dist/${name}-[hash].js`;
                },
                assetFileNames: (chunkInfo) => {
                    const [module, name] = chunkInfo.name.split('/');
                    
                    return `${module}/static/dist/${name}`;
                }
            }
        }
    }
})