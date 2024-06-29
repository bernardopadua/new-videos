INSERT INTO public.nvideo_user
(
	user_name, user_surname, user_email, 
	user_password, user_birth_date, user_avatar_url, 
	user_permission, user_is_active, updated_by, 
	created_by, created_at, updated_at
)
VALUES(
	'Test3', 'Test', 'email3@test.com.br', 
	'123456', '1989-07-18', '', 
	E'\x02', true, 1, 1, NOW(), NOW()
);


INSERT INTO public.channel
(
	channel_name, channel_description, 
	channel_image_url, channel_avatar_url, 
	user_id, updated_by, created_by, created_at, updated_at
)
VALUES(
	'Name test', 'Test channel to test', 
	'', '', 
	1, 1, 1, NOW(), NOW());


INSERT INTO public.subscriber
(
	channel_id, user_id, subscriber_is_active, 
	updated_by, created_by, created_at, updated_at
)
VALUES(
	1, 2, true, 1, 1, now(), now()
);
