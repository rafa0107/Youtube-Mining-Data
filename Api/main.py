# Programa principal
from src.services.youtube_services import YoutubeService
import pandas as pd

if __name__ == "__main__":
    service = YoutubeService()

    data = service.collect_videos("Inteligencia Artificial", max_pages=1)

    for video in data:
        print(video["title"])
        print("Views:", video["views"])
        print("Likes:", video["likes"])
        print("Comentarios:", video["comments"])
        print("---------------")
    
    #Salvando em CSV com o pandas
    df = pd.DataFrame(data)
    df.to_csv("data/raw/videos.csv", index=False)