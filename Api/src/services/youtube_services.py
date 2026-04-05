# Onde será implementado a lógica do négocio (Pipelines de Mineração)
from src.api.youtube_client import YoutubeClient

#Camada de lógica do sistema.
class YoutubeService:
    def __init__ (self):
        self.client = YoutubeClient()

    def get_videos_with_stats(self, query):
        search_data = self.client.search_videos(query)

        videos_id = [
            item["id"]["videoId"]
            for item in search_data["items"]
        ]

        details = self.client.get_video_details(videos_id)
        return details

    def collect_videos(self, query, max_pages=3):
        all_data = []
        next_page = None

        for page in range(max_pages):
            #print de pagina para debug
            print(f"\n ----- Página {page +1 } ------ ")

            search_data = self.client.search_videos(query,  page_token=next_page)
            print(search_data)
            videos_id = [item["id"]["videoId"] for item in search_data["items"]]
            details = self.client.get_video_details(videos_id)

            for video in details["items"]:
                video_id = video["id"]
            
                #Print para debuggar
                print(f"Coletando vídeo: {video_id}")

                #Coletar comentários
                try:
                    comments = self.client.get_top_comments(video_id)
                    comment_list = [
                        c["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                        for c in comments.get("items", [])
                    ]
                except Exception as e:
                    print(f"Erro ao pegar comentários do vídeo {video_id}: {e}")
                    comment_list = []


                video_data = {
                    "video_id": video_id,   
                    "title": video["snippet"]["title"],
                    "channel": video["snippet"]["channelTitle"],
                    "published_at": video["snippet"]["publishedAt"],
                    "views": video["statistics"].get("viewCount"),
                    "likes":video["statistics"].get("likeCount"),
                    "comments_count": video["statistics"].get("commentCount"),
                    "duration": video.get("contentDetails", {}).get("duration"),
                    "comments": " | ".join(comment_list)
                }

                all_data.append(video_data)
            
            next_page = search_data.get("nextPageToken")

            if not next_page:
                break
        
        return all_data
