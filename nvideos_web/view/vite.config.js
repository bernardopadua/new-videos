import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import obfuscator from 'rollup-plugin-obfuscator';
import fs from 'node:fs';

const cleanSomeDirs = () => ({
    name: 'clean-some-dirs',
    buildStart: () => {
        const dirs = [
            'base/static/dist',
            'channel_details/static/dist',
            'video_details/static/dist',
            'user_details/static/dist',
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
        outDir: '.', //I know you can't be root dir. But I'm experimenting. Hold on.
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
                'base/base_entry/bs': './base/entries/base_entry.js',

                //Home
                'home/avatar_entry': './home/entries/avatar_entry.jsx',
                'home/user_register_form_validation/ufrv': './home/entries/user_registration/user_register_form_validation.js',
                'home/user_login/login': './home/entries/user_login/user_login.js',
                'home/home_videos_entry/hve': './home/entries/home_videos_entry.jsx',

                //UserDetails
                'user_details/avatar_upload_user_details/ausd': './user_details/entries/avatar_upload_user_details.jsx',
                'user_details/user_edit_details/ued': './user_details/entries/user_edit_details/user_edit_details.js',

                //ChannelDetails
                'channel_details/channel_editcreate_details/ced': './channel_details/entries/channel_editcreate_details_entry.jsx',
                'channel_details/channel_detail/cde': './channel_details/entries/channel_detail_entry.jsx',

                //VideoDetails
                'video_details/video_details_entry/vde': './video_details/entries/video_details_entry.jsx',
                'video_details/video_details_registration_editing/vdre': './video_details/entries/video_details_registration_editing.js',
                'video_details/video_listing_entry/vle': './video_details/entries/video_listing_entry.jsx',
                'video_details/video_detail_watch_entry/vdwe': './video_details/entries/video_detail_watch_entry.jsx',
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