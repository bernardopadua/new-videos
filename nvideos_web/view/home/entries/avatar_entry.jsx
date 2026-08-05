import React from 'react';
import ReactDOM from 'react-dom/client';
import AvatarUpload from '../components/AvatarUpload';

const container = document.getElementById('avatar-root');

if (container) {
    ReactDOM.createRoot(container).render(
        <React.StrictMode>
            <AvatarUpload />
        </React.StrictMode>
    );
}
