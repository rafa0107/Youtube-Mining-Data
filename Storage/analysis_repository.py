from database import get_connection

class AnalysisRepository:
    def get_most_liked_comments(self, limit=10):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM view_analise_completa ORDER BY likes_comentario DESC LIMIT %s"
        cursor.execute(query, (limit,))
        return cursor.fetchall()