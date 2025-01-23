import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='G:\Meu Drive\Development\sylphie\.venv\.env')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_PORT= os.getenv('DB_PORT')
DB_DSN= os.getenv('DB_DSN')
ORA_PATH= os.getenv('ORACLE_LIB')

def query(sql: str) -> list:
        data = 'dados'
        return data
    
# print(query("select * from TMP_ACOES_COMERCIAIS where rownum <5"))

def diffusion_query(date: str, werks: str) -> list:
    sql = f"SELECT * FROM BI_DW.VOLUME_DIFUSAO_PRECO WHERE data_de IN TO_DATE('{date}', 'dd/mm/YY') AND WERKS IN ('{werks}')"
    diffusion_table = query(sql)
    return diffusion_table

def products_query(skus) -> list:
    sql = f"""SELECT * FROM BI_DW.PRODUTOS WHERE COD_PRODUTO IN ({skus})"""
    products_table = query(sql)
    return products_table