-- Base user permissions so far
insert into user_permission (user_permission, permission_description) values (E'\x1', 'User with system access. Is used by the system and has access to every part of the system. A Superuser.');
insert into user_permission (user_permission, permission_description) values (E'\x2', 'Normal user access.');

-- Base video permissions so far
insert into video_permission (video_permission, permission_description) values (E'\x1', 'Public video. Everybody can access.');
insert into video_permission (video_permission, permission_description) values (E'\x2', 'Private video. Only the author has access.');
insert into video_permission (video_permission, permission_description) values (E'\x3', 'Only for subscribers.');
insert into video_permission (video_permission, permission_description) values (E'\x4', 'Only accessible through a link.');