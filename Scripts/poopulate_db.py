import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from load_data import load_data_videos, load_data_comments
from Storage.video_repository import VideoRepository
from Storage.comment_repository import CommentRepository

file_path_videos = "../Api/data/processed/processed_videos.csv"
file_path_comments = "../Api/data/raw/comments.csv"

def main():
    video_repo = VideoRepository()
    comment_repo = CommentRepository()

    videos_data = load_data_videos(file_path_videos)
    comments_data = load_data_comments(file_path_comments)
    
    if videos_data:
        print("Inserindo vídeos no banco de dados...")
        for video in videos_data:
            video_repo.save_video(video)

    
    if comments_data:
        print("Inserindo comentários no banco de dados...")
        for comment in comments_data:
            comment_repo.save_comment(comment)
    else:
        print("Nenhum comentário para inserir.")

if __name__ == "__main__":
    main()