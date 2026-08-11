ALTER TABLE video 
    ADD COLUMN video_status VARCHAR(11) NOT NULL DEFAULT 'uploaded',
    ADD COLUMN video_temp_filename VARCHAR(50);
