from database import get_connection

def create_analytics_views():
    """Cria todas as visualizações necessárias para análise de dados."""
    queries = {
        "view_analise_completa": """
            CREATE OR REPLACE VIEW view_analise_completa AS
            SELECT 
                v.video_id,
                v.title AS video_titulo,
                v.channel_title AS canal,
                c.author_display_name AS autor_comentario,
                c.text_display AS comentario_texto,
                c.like_count AS likes_comentario
            FROM comments c
            JOIN videos v ON c.video_id = v.video_id;
        """,
    }

    conn = get_connection()
    try:
        cursor = conn.cursor()
        for name, sql in queries.items():
            cursor.execute(sql)
            print(f"✅ View '{name}' configurada com sucesso.")
        conn.commit()
    except Exception as e:
        print(f"❌ Erro ao configurar Views: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_analytics_views()