# Programa principal
from src.services.youtube_services import YoutubeService
import pandas as pd
import os

if __name__ == "__main__":
    service = YoutubeService()
    data = service.collect_videos("estreito de ormuz", max_pages=15)

    # Define as colunas que quero salvar na ordem correta (conforme SQL)
    cols_videos = ["video_id", "title", "published_at", "channel_id", "channel_title", "view_count", "like_count", "category", "comment_count"]
    cols_comments = ["video_id", "author_display_name", "text_display", "published_at", "like_count"]

    #1. Processar VÍDEOS
    df_videos = pd.DataFrame(data["videos"])
    path_videos = "data/raw/videos.csv"
    
    if os.path.exists(path_videos):
        old_df = pd.read_csv(path_videos)
        df_videos = pd.concat([old_df, df_videos], ignore_index=True)
    
    # Remove duplicatas baseando-se no ID único do vídeo
    df_videos = df_videos.drop_duplicates(subset=["video_id"], keep="last")
    
    df_videos.to_csv(path_videos, index=False)

    #2. Processar COMENTÁRIOS
    df_comments = pd.DataFrame(data["comments"])
    path_comments = "data/raw/comments.csv"
    
    if os.path.exists(path_comments):
        old_comments = pd.read_csv(path_comments)
        df_comments = pd.concat([old_comments, df_comments], ignore_index=True)
    
    # Como não possui o comment_id, usei o autor, o texto e o video_id 
    # para garantir que o mesmo comentário não seja inserido duas vezes.
    if not df_comments.empty:
        df_comments = df_comments.drop_duplicates(
            subset=["video_id", "author_display_name", "text_display"], 
            keep="first"
        )
    
    df_comments.to_csv(path_comments, index=False)
    print(f"Salvo: {len(df_comments)} comentários em {path_comments}")