#Dados SQL de videos
from Storage.database import get_connection

class VideoRepository:
      
    def save_video(self, video_data):

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT IGNORE INTO videos (video_id, title, published_at, channel_id, channel_title,view_count,like_count,category,comment_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                video_data.get('video_id'),
                video_data.get('title'),
                video_data.get('published_at'),
                video_data.get('channel_id'),
                video_data.get('channel_title')
                ,video_data.get('view_count'),
                video_data.get('like_count'),
                video_data.get('category'),
                video_data.get('comment_count'),
            ))
            conn.commit()
            print(f"Vídeo '{video_data.get('title')}' salvo com sucesso.")

        except Exception as e:
            print(f"Erro ao salvar vídeo: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


