import { ROUTES } from "../../../base/entries/constants/routes";

export default function VideoSubscribe() {
    const subscribeBtn = document.getElementById("btn-subscribe-channel");
    const unsubscribeBtn = document.getElementById("btn-unsubscribe-channel");
    const channelSubscribers = document.getElementById("channel-subscribers");
    const initialData = JSON.parse(document.getElementById("initial-data-subscribe").text);
    
    const channelId = initialData?.channelId;
    const userOwnChannel = initialData?.userOwnChannel;

    if(!userOwnChannel){
        fetch(ROUTES.isSubscribedChannel(channelId))
            .then((r) => r.json())
            .then((d) => {
                if (d?.isSubscribed) {
                    subscribeBtn.classList.add("hidden");
                    unsubscribeBtn.classList.remove("hidden");
                } else {
                    subscribeBtn.classList.remove("hidden");
                    unsubscribeBtn.classList.add("hidden");
                }
            });
        
        const updateTotalSubscribers = () => {
            fetch(ROUTES.totalSubscribedChannel(channelId))
                .then((r) => r.json())
                .then((d) => {
                    if (d?.totalSubscribers) {
                        channelSubscribers.innerText = d.totalSubscribers;
                    } else if (d?.error) {
                        console.error(d?.error);
                    }
                });
        };

        subscribeBtn.addEventListener("click", () => {
            fetch(ROUTES.subscribeChannel(channelId), {
                method: "POST"
            })
                .then((r) => r.json())
                .then((d) => {
                    if (d?.isSubscribed) { 
                        subscribeBtn.classList.add("hidden");
                        unsubscribeBtn.classList.remove("hidden");

                        updateTotalSubscribers();
                    }
                });
        });
        unsubscribeBtn.addEventListener("click", () => {
            fetch(ROUTES.unsubscribeChannel(channelId), {
                method: "POST"
            })
                .then((r) => r.json())
                .then((d) => {
                    if (d?.isUnsubscribed) { 
                        subscribeBtn.classList.remove("hidden");
                        unsubscribeBtn.classList.add("hidden");

                        updateTotalSubscribers();
                    }
                });
        });
    }
};