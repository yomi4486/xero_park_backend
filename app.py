from os.path import join, dirname
from dotenv import load_dotenv
import fastapi,json,os, psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
env = os.environ
connection = psycopg2.connect(
    host=env.get("DB_ADDRESS"),
    user=env.get("DB_USER"),
    password=env.get("DB_PASS"),
    database=env.get("DB_NAME")
)

@app.post("/post")
def post(token:str="",title:str="",datail:str="",tags:list=[]):
    with connection:
        with connection.cursor() as cursor:
            sql = f"""
                INSERT INTO testdb (
                    id, 
                    title,
                    datail,
                    author,
                    firsttime,
                    lastedit,
                    tags,
                ) VALUES (
                    
            )"""
            cursor.execute(sql)
    
        # コミットしてトランザクション実行
        connection.commit()