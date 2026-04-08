DROP DATABASE IF EXISTS youtube_mining_data;
CREATE DATABASE youtube_mining_data;
USE youtube_mining_data;

CREATE TABLE IF NOT EXISTS videos (
    video_id VARCHAR(255) PRIMARY KEY,
    title TEXT,
    published_at DATETIME,
    channel_id VARCHAR(255),
    channel_title VARCHAR(255),
    view_count BIGINT,
    like_count BIGINT,
    category VARCHAR(255),
    comment_count INT
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    video_id VARCHAR(255),
    author_display_name VARCHAR(255),
    text_display TEXT,
    published_at DATETIME,
    like_count INT,
    FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE
);

