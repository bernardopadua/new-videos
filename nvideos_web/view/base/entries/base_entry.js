document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('user-menu-button');
    const dropdown = document.getElementById('user-menu-dropdown');
    const container = document.getElementById('user-menu-container');

    const mainContent = document.getElementById('main-content');
    const asideMenuButton = document.getElementById('aside-menu-button');
    const asideMenu = document.getElementById('aside-menu');

    if (menuButton && dropdown) {
        menuButton.addEventListener('click', (e) => {
            e.stopPropagation();
            const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
            menuButton.setAttribute('aria-expanded', !isExpanded);
            dropdown.classList.toggle('hidden');
        });

        document.addEventListener('click', (e) => {
            if (container && !container.contains(e.target)) {
                menuButton.setAttribute('aria-expanded', 'false');
                dropdown.classList.add('hidden');
            }
        });
    }

    if (asideMenuButton) {
        asideMenuButton.addEventListener('click', (e) => {
            const isLg = window.matchMedia("(min-width: 1024px)").matches;
            if (isLg) {
                asideMenu.classList.add('hidden');
                if (asideMenu.classList.contains('lg:block')) {
                    asideMenu.classList.remove('lg:block');
                    mainContent.classList.remove('lg:pl-60');
                } else {
                    asideMenu.classList.add('lg:block');
                    mainContent.classList.add('lg:pl-60');
                }
            } else {
                asideMenu.classList.toggle('hidden');
            }
        });
    }

});