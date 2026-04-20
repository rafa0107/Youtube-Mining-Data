import pandas as pd
import numpy as np


file_path_videos = "../Api/data/processed/processed_videos.csv"
file_path_comments = "../Api/data/processed/processed_comments.csv"


#Lê o CSV e converte para um dicionário, retorna formato esperado para repositórios
def load_data_videos(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso de {file_path}")
        df = pd.DataFrame(data)
        df = df.replace({np.nan: None})
        data_dict = df[['video_id', 'title', 'published_at', 'channel_id', 'channel_title', 'view_count', 'like_count', 'category', 'comment_count']].to_dict(orient='records')
        return data_dict
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None
    
def load_data_comments(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso de {file_path}")
        df = pd.DataFrame(data)
        df = df.replace({np.nan: None})
        data_dict = df[['video_id', 'author_display_name', 'text_display', 'published_at', 'like_count']].to_dict(orient='records')
        return data_dict
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None


