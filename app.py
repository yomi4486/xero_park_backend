from os.path import join, dirname
from dotenv import load_dotenv
import fastapi,json,os, psycopg2,datetime
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
def post(token:str="",title:str="",datail:str="",content:str="",tags:list=[]):
    dt_now = datetime.datetime.now()
    now_timestamp = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO testdb (title,datail,author,firsttime,lastedit,tags,content) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            # TODO: usernameはtokenから取得する。
            cursor.execute(sql,(title,datail,"username",now_timestamp,now_timestamp,tags,content))
    
        # コミットしてトランザクション実行
        connection.commit()