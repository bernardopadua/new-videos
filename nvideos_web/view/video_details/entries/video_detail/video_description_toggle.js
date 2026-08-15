export default function VideoDescriptionToggle() {
    const descWrapper = document.getElementById('desc-wrapper');
    const descFade = document.getElementById('desc-fade');
    const descMore = document.getElementById('desc-more');
    
    if (descWrapper.hasAttribute('has-more') && descFade) {
        descMore.addEventListener('click', () => {
            const height = descWrapper.scrollHeight;
            
            if (descWrapper.classList.contains('max-h-20')) {
                descWrapper.classList.remove('max-h-20');
                descFade.classList.add('hidden');
                descMore.textContent = '...less';
            } else {
                descWrapper.classList.add('max-h-20');
                descFade.classList.remove('hidden');
                descMore.textContent = '...more';
            }
        });
    }
}