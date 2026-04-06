# Programa principal
from src.services.youtube_services import YoutubeService
import pandas as pd
import os

if __name__ == "__main__":
    service = YoutubeService()

    data = service.collect_videos("Inteligência Artificial", max_pages=15)

    for video in data:
        print(video["title"])
        print("Views:", video["views"])
        print("Likes:", video["likes"])
        print("Comentarios:", video["comments"])
        print("---------------")
    
    #Salvando em CSV com o pandas
    if (os.path.exists("data/raw/videos.csv")):
        df = pd.read_csv("data/raw/videos.csv")
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        os.makedirs("data/raw", exist_ok=True)
        df = pd.DataFrame(data)
    
    df = df.drop_duplicates(subset="video_id")
    df.to_csv("data/raw/videos.csv", index=False)