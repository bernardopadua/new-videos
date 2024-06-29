alter table subscriber 
add constraint subscriber_unique_subscriber unique (channel_id, user_id);