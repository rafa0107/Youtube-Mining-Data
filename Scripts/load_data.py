import pandas as pd


file_path = "../Api/data/raw/videos.csv"

#Lê o CSV e converte para um dicionário, retorna formato esperado para repositórios
def load_data_videos(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso de {file_path}")
        df = pd.DataFrame(data)
        data_dict = df[['video_id', 'title', 'channel', 'published_at', 'views', 'likes', 'comments_count', 'duration']].to_dict(orient='records')
        return data_dict
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None
    
def load_data_comments(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso de {file_path}")
        df = pd.DataFrame(data)
        data_dict = df[['video_id', 'title', 'channel', 'published_at', 'views', 'likes', 'comments_count', 'duration']].to_dict(orient='records')
        return data_dict
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

#video_id,title,channel,published_at,views,likes,comments_count,duration,comments

