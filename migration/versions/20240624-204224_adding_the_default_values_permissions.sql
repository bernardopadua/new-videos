-- Base user permissions so far
insert into user_permission (user_permission, permission_description) values (E'\x0', 'User with system access. Is used by the system and has access to every part of the system. A Superuser.');
insert into user_permission (user_permission, permission_description) values (E'\x1', 'Normal user access.');

-- Base video permissions so far
insert into video_permission (video_permission, permission_description) values (E'\x0', 'Public video. Everybody can access.');
insert into video_permission (video_permission, permission_description) values (E'\x1', 'Private video. Only the author has access.');
insert into video_permission (video_permission, permission_description) values (E'\x2', 'Only for subscribers.');
insert into video_permission (video_permission, permission_description) values (E'\x3', 'Only accessible through a link.');