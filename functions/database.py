import oracledb
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='G:\Meu Drive\Development\sylphie\.venv\.env')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_PORT= os.getenv('DB_PORT')
DB_DSN= os.getenv('DB_DSN')
ORA_PATH= os.getenv('ORACLE_LIB')

oracledb.init_oracle_client(lib_dir=rf"{ORA_PATH}")

pool = oracledb.create_pool(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN,
                            min=1, max=5, increment=1)

def query(sql: str):
    data = []
    with pool.acquire() as conn:
        with conn.cursor() as cursor:
            for result in cursor.execute(sql):
                data.append(result)
        return data
    
# print(query("select * from TMP_ACOES_COMERCIAIS where rownum <5"))

def diffusion_query(date, werks):
    sql = f"SELECT * FROM BI_DW.VOLUME_DIFUSAO_PRECO WHERE data_de IN ('{date}') AND WERKS IN ('{werks}')"
    diffusion_table = query(sql)
    return diffusion_table