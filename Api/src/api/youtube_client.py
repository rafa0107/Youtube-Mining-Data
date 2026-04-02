# Comunicação direta com o youtube, requisições HTTP
import requests
from src.utils.config import API_KEY, BASE_URL

class YoutubeClient:

    #Camada de acesso à API do Youtube, irá fazer as requisições
    #Define os videos que irei buscar, a quantidade de retorno das buscas e parametros.
    def search_videos(self, query, max_results=50, page_token=None, published_after=None, published_before=None):
        url = f"{BASE_URL}/search"

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order" : "date",
            "maxResults": max_results,
            "key": API_KEY
        }

        #Lógica para mudança de página
        if page_token:
            params["pageToken"] = page_token
        
        if published_after:
            params["publishedAfter"] = published_after
        
        if published_before:
            params["publishedBefore"] = published_before

        response = requests.get(url, params=params)
        return response.json()

    #Lógica para buscar detalhes de cada vídeo.
    def get_video_details(self, video_ids):
        url = f"{BASE_URL}/videos"

        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids),
            "key": API_KEY
        }

        response = requests.get(url, params=params)
        return response.json()
    
    #Lógica para buscar os top comentarios de cada vídeo.
    def get_top_comments(self, video_id):
        url = f"{BASE_URL}/commentThreads"

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 10,
            "order": "relevance",
            "key": API_KEY
        }

        response = requests.get(url, params=params)
        return response.json()
    