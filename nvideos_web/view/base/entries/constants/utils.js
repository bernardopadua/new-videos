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