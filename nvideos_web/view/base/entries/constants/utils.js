export function formatDuration(seconds) {
    if (!seconds) return "00:00";
    
    const hours = seconds > 3600 ? Math.floor(seconds / 3600) : '00';
    const minutes = seconds > 3600 ? Math.floor((seconds % 3600) / 60).toString().padStart(2, '0') : Math.floor(seconds / 60).toString().padStart(2, '0');
    const secs = Math.round(seconds % 60).toString().padStart(2, '0');

    return hours !== '00' ? `${hours}:${minutes}:${secs}` : `${minutes}:${secs}`;
};

export function formatViews(views) {
    if (!views) return "0 views";
    const formatted = new Intl.NumberFormat('en-US', {
        notation: 'compact',
        compactDisplay: 'short'
    }).format(views);
    
    return `${formatted} views`;
}

export function formatDatetimeToString(dateTime) {
    if (!dateTime) return "";
    const dt = new Date(dateTime);
    if (isNaN(dt.getTime())) return "";

    const year = dt.getFullYear();
    const month = String(dt.getMonth() + 1).padStart(2, '0');
    const day = String(dt.getDate()).padStart(2, '0');
    const hours = String(dt.getHours()).padStart(2, '0');
    const minutes = String(dt.getMinutes()).padStart(2, '0');
    const seconds = String(dt.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
