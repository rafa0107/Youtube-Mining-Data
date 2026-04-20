#Dados SQL de comentarios
from Storage.database import get_connection

class CommentRepository:
    def save_comment(self, comment_data):

        if not comment_data or not comment_data.get('text_display'):
            print("Comentário ignorado (vazio ou inválido).")
            return

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT IGNORE INTO comments (video_id, author_display_name, text_display, published_at, like_count)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                comment_data.get('video_id'),
                comment_data.get('author_display_name'),
                comment_data.get('text_display'),
                comment_data.get('published_at'),
                comment_data.get('like_count'),
            ))

            conn.commit()
            print(f"Comentário '{comment_data.get('video_id')}' salvo com sucesso.")

        except Exception as e:
            print(f"Erro ao salvar comentário: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()