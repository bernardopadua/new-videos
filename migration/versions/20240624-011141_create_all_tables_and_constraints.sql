create table nvideo_user (
	user_id serial primary key,
	user_name varchar(100) not null,
	user_surname varchar(150) not null,
	user_email varchar(150) not null,
	user_password varchar(300) not null,
	user_birth_date date,
	user_avatar_url varchar(400),
	user_permission char(1) not null, -- edit videos (that I dont own), edit comments, delete and etc...
	user_is_active bool not null,
	updated_by int,
	created_by int,
	created_at timestamptz not null,
	updated_at timestamptz
);

create table user_permission (
	user_permission char(1) primary key,
	permission_description varchar(250) not null
);

create table notification_module (
	notification_module varchar(15) primary key,
	module_description varchar(150) not null
);

create table notification (
	notification_id serial primary key,
	user_id int not null,
	notification_module varchar(15) not null,
	notification_description varchar(200) not null
);

create table channel (
	channel_id serial primary key,
	channel_name varchar(150) not null,
	channel_description text,
	channel_image_url varchar(500),
	channel_avatar_url varchar(500),
	channel_is_active bool not null,
	user_id int not null,
	updated_by int,
	created_by int not null,
	created_at timestamptz not null,
	updated_at timestamptz
);

create table subscriber (
	subscriber_id serial primary key,
	channel_id int not null,
	user_id int not null,
	subscriber_is_active bool not null,
	updated_by int,
	created_by int not null,
	created_at timestamptz not null,
	updated_at timestamptz
);

create table video (
	video_id serial primary key,
	video_title varchar(200) not null,
	video_description text,
	video_time_duration int,
	video_view_count int not null,
	video_thumb_url varchar(500),
	video_tags varchar(20)[],
	video_permission char(1), -- It will be accessed publicly, private, members-only, members-first...
	channel_id int not null,
	user_id int not null,
	updated_by int,
	created_by int not null,
	created_at timestamptz not null,
	updated_at timestamptz
);

create table video_permission (
	video_permission char(1) primary key,
	permission_description varchar(250) not null
);

create table nvideo_comment (
	comment_id serial primary key,
	video_id int not null,
	user_id int not null,
	comment_description text not null,
	comment_comment_id int,
	updated_by int,
	created_by int not null,
	created_at timestamptz not null,
	updated_at timestamptz
);

-- ### Applying constrains ###

-- #> USER
alter table nvideo_user 
add constraint fk_user_user_permission 
foreign key (user_permission) references user_permission(user_permission);

alter table nvideo_user 
add constraint fk_user_created_user 
foreign key (created_by) references nvideo_user(user_id);
alter table nvideo_user 
add constraint fk_user_updated_user 
foreign key (updated_by) references nvideo_user(user_id);

-- --------------------------------

-- #> CHANNEL
-- User -> Channel
alter table channel 
add constraint fk_user_channel 
foreign key (user_id) references nvideo_user(user_id);

--->> Audit
alter table channel 
add constraint fk_user_created_channel 
foreign key (created_by) references nvideo_user(user_id);
alter table channel 
add constraint fk_user_updated_channel 
foreign key (updated_by) references nvideo_user(user_id);

-- --------------------------------

-- #> NOTIFICATION
-- User -> Notification
alter table notification 
add constraint fk_user_notification 
foreign key (user_id) references nvideo_user(user_id);
-- NotificationModule -> Notification
alter table notification
add constraint fk_notification_module_notification 
foreign key (notification_module) references notification_module(notification_module);

-- --------------------------------

-- #> SUBSCRIBER
-- Channel -> Subscriber
alter table subscriber 
add constraint fk_channel_subscriber 
foreign key (channel_id) references channel(channel_id);
-- User -> Subscriber
alter table subscriber 
add constraint fk_user_subscriber 
foreign key (user_id) references nvideo_user(user_id);

-- Unique Constraint
alter table subscriber 
add constraint unq_user_subscribe_channel
unique (user_id, channel_id);

--->> Audit
alter table subscriber 
add constraint fk_user_created_subscriber 
foreign key (created_by) references nvideo_user(user_id);
alter table subscriber 
add constraint fk_user_updated_subscriber 
foreign key (updated_by) references nvideo_user(user_id);

-- --------------------------------

-- #> VIDEO
-- User -> Video
alter table video 
add constraint fk_user_video 
foreign key (user_id) references nvideo_user(user_id);
-- Channel -> Video
alter table video 
add constraint fk_channel_video 
foreign key (channel_id) references channel(channel_id);
-- VideoPermission -> Video
alter table video 
add constraint fk_video_permission_video 
foreign key (video_permission) references video_permission(video_permission);

--->> Audit
alter table video 
add constraint fk_user_created_video 
foreign key (created_by) references nvideo_user(user_id);
alter table video 
add constraint fk_user_updated_video 
foreign key (updated_by) references nvideo_user(user_id);

-- --------------------------------

-- #> VIDEO
-- User -> Comment
alter table nvideo_comment 
add constraint fk_user_comment 
foreign key (user_id) references nvideo_user(user_id);
-- Video -> Comment
alter table nvideo_comment 
add constraint fk_video_comment 
foreign key (video_id) references video(video_id);
-- Comment -> Comment
alter table nvideo_comment 
add constraint fk_comment_comment 
foreign key (comment_comment_id) references nvideo_comment(comment_id);

--->> Audit
alter table nvideo_comment 
add constraint fk_user_created_comment 
foreign key (created_by) references nvideo_user(user_id);
alter table nvideo_comment 
add constraint fk_user_updated_comment 
foreign key (updated_by) references nvideo_user(user_id);
