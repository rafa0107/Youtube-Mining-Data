from datetime import datetime
import os
import pandas as pd


file_path_videos = "../raw/videos.csv"
file_path_comments = "../raw/comments.csv"


def transform_videos(file_path):
    if not file_path:
        print("Caminho do arquivo não fornecido.")
        return None
    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0).astype(int)
    df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce').fillna(0).astype(int)
    return df

df_transformed_videos = transform_videos(file_path_videos)
if df_transformed_videos is not None:
    processed_csv = df_transformed_videos.to_csv("processed_videos.csv", index=False)

def transform_comments(file_path):
    if not file_path:
        print("Caminho do arquivo não fornecido.")
        return None
    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0).astype(int)
    return df


df_transformed_comments = transform_comments(file_path_comments)
if df_transformed_comments is not None:
    processed_csv = df_transformed_comments.to_csv("processed_comments.csv", index=False)