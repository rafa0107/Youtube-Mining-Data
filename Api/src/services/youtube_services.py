# Onde será implementado a lógica do négocio (Pipelines de Mineração)
from src.api.youtube_client import YoutubeClient

#Camada de lógica do sistema.
class YoutubeService:
    def __init__ (self):
        self.client = YoutubeClient()
        self.category_map = {}

    
    def get_category_name(self, category_id):
        # Se o ID já está no dicionário, não gasta API
        if category_id in self.category_map:
            return self.category_map[category_id]

        # Se não está, busca na API (Apenas uma vez por categoria)
        try:
            print(f"Buscando nome da categoria {category_id} na API...")
            response = self.client.get_categories(category_id)
            # Extrai o título
            name = response['items'][0]['snippet']['title']
            self.category_map[category_id] = name
            return name
        except:
            return "Unknown"

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
        all_comments = []
        next_page = None

        for page in range(max_pages):
            #print de pagina para debug
            print(f"\n ----- Página {page +1 } ------ ")

            search_data = self.client.search_videos(query,  page_token=next_page)

            videos_id = []
            for item in search_data.get("items", []):
                # Verifica se o id é um dicionário e se tem o videoId
                v_id = item.get("id", {}).get("videoId")
                if v_id:
                    videos_id.append(v_id)

            if not videos_id:
                print(f"Aviso: Nenhum vídeo encontrado na página {page + 1}")
                break

            details = self.client.get_video_details(videos_id)

            for video in details["items"]:
                video_id = video["id"]

                #Print para debuggar
                print(f"Coletando vídeo: {video_id}")

                cat_id = video["snippet"].get("categoryId")
                cat_name = self.get_category_name(cat_id)

                video_data = {
                    "video_id": video_id,   
                    "title": video["snippet"]["title"],
                    "published_at": video["snippet"]["publishedAt"],
                    "channel_id": video["snippet"]["channelId"],
                    "channel_title": video["snippet"]["channelTitle"],
                    "view_count": video["statistics"].get("viewCount"),
                    "like_count": video["statistics"].get("likeCount"),
                    "category": cat_name,
                    "comment_count": video["statistics"].get("commentCount")
                }

                all_data.append(video_data)

                snippet = video.get("snippet", {})
                try:
                    comments_response = self.client.get_top_comments(video_id)
                    for c in comments_response.get("items", []):
                        snippet = c["snippet"]["topLevelComment"]["snippet"]
                    
                    comment_entry = {
                        "video_id": video_id,
                        "author_display_name": snippet.get("authorDisplayName"),
                        "text_display": snippet.get("textDisplay"),
                        "published_at": snippet.get("publishedAt"),
                        "like_count": snippet.get("likeCount")
                    }
                    all_comments.append(comment_entry)
                except Exception as e:
                    print(f"Comentários desativados ou erro no vídeo {video_id}: {e}")

            next_page = search_data.get("nextPageToken")

            if not next_page:
                break
        
        return {"videos": all_data, "comments": all_comments}
