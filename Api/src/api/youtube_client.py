# Comunicação direta com o youtube, requisições HTTP
import requests
from src.utils import API_KEY, BASE_URL

class YoutubeClient:


    #Define os videos que irei buscar, a quantidade de retorno das buscas e parametros.
    def search_videos(self, query, max_results=5):
        url = f"{BASE_URL}/search"

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": API_KEY
        }

        response = requests.get(url, params=params)
        return response.json

    #Define a url de cada vidbuscar os detalhes de cada um.
    def get_video_details(self, video_ids):
        url = f"{BASE_URL}/videos"
    