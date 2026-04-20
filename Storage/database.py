#Criacao do Database
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os


load_dotenv()

def get_connection():
    cnx = None
    try:
        cnx = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception("Erro de autenticação: Verifique seu nome de usuário ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise Exception("Erro de banco de dados: O banco de dados especificado não existe.")
        else:
            raise Exception("Erro ao conectar ao banco de dados.")
    else:
        print("Conexão bem-sucedida ao banco de dados!")
        
    return cnx
