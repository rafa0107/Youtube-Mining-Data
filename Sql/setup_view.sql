USE youtube_mining_data;

CREATE OR REPLACE VIEW view_engajamento_videos AS
SELECT 
    video_id,
    title,
    view_count,
    like_count,
    comment_count,
    (like_count / view_count) * 100 AS taxa_engajamento
FROM videos
WHERE view_count > 0;

CREATE OR REPLACE VIEW view_analise_completa AS
SELECT 
    v.title AS video_titulo,
    c.author_display_name AS autor,
    c.text_display AS comentario
FROM comments c
JOIN videos v ON c.video_id = v.video_id;