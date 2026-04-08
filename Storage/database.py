#Criacao do Database
import mysql.connector


def get_connection():
    cnx = None
    try:
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='youtube_mining_data'
        )
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception("Erro de autenticação: Verifique seu nome de usuário ou senha.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            raise Exception("Erro de banco de dados: O banco de dados especificado não existe.")
        else:
            raise Exception("Erro ao conectar ao banco de dados.")
    else:
        print("Conexão bem-sucedida ao banco de dados!")
        
    return cnx

conn = get_connection()
print(conn)