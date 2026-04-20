from analysis_repository import AnalysisRepository

def main():
    analysis_repo = AnalysisRepository()

    print("--- 🏆 TOP 5 COMENTÁRIOS COM MAIS LIKES ---")
    
    top_comments = analysis_repo.get_most_liked_comments(limit=5)

    if not top_comments:
        print("Nenhum dado encontrado na View.")
        return

    for idx, row in enumerate(top_comments, 1):
        print(f"{idx}. [{row['canal']}] - Vídeo: {row['video_titulo'][:50]}...")
        print(f"   Autor: {row['autor_comentario']}")
        print(f"   Likes: {row['likes_comentario']}")
        print(f"   Texto: {row['comentario_texto'][:100]}")
        print("-" * 30)

if __name__ == "__main__":
    main()