from os.path import join, dirname
from dotenv import load_dotenv
import fastapi,json,os, psycopg2,datetime
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from fastapi import HTTPException 

class UserData(BaseModel): 
    token: str 
    title: str
    datail: str
    content: str
    tags: str

class DeleteFormat(BaseModel): 
    token: str 
    id: int

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*","DELETE"],
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
def post(user_data: UserData):
    print("Post ok!",flush=True)
    dt_now = datetime.datetime.now()
    now_timestamp = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO test (title,datail,author,firsttime,lastedit,tags,content) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;"
            # TODO: usernameはtokenから取得する。
            cursor.execute(sql,(user_data.title,user_data.datail,user_data.token,now_timestamp,now_timestamp,user_data.tags,user_data.content))
            inserted_id = cursor.fetchone()[0]
            print(inserted_id,flush=True)
        # コミットしてトランザクション実行
        connection.commit()
    return inserted_id

@app.get("/read")
def read(id:int):
    print(f"read ok:{id}",flush=True)
    sql = f"SELECT * FROM test WHERE id = {id};"
    try:
        with connection:
            with connection.cursor() as cursor:
                # TODO: usernameはtokenから取得する。
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    content = dict(zip(columns,row))
                else:
                    raise HTTPException(status_code=404, detail="Page not found!")
        print(f"コンテンツ：{content}",flush=True)
        return content
    except:
        raise HTTPException(status_code=404, detail="Page not found!")

@app.get("/get_user_page") # 投稿者がユーザーIDと一致するページを一括取得
def get_user_page(id: str):
    sql = f"SELECT * FROM test WHERE author = '{id}';"
    try:
        with connection:
            with connection.cursor() as cursor:
                # TODO: usernameはtokenから取得する。
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    columns = [desc[0] for desc in cursor.description]
                    content = [dict(zip(columns, row)) for row in rows]
                else:
                    raise HTTPException(status_code=404, detail="Page not found!")
        print(f"コンテンツ：{content}", flush=True)
        return content
    except:
        raise HTTPException(status_code=404, detail="Page not found")
    
@app.delete('/delete_page')
def delete_page(user_data:DeleteFormat):
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM test WHERE id = %s AND author = %s;"
                # TODO: usernameはtokenから取得する。
                cursor.execute(sql,(user_data.id,user_data.token))
            # コミットしてトランザクション実行
            connection.commit()
    except Exception as e:
        print(e,flush=True)
        raise HTTPException(status_code=401, detail="permission denied")
    return {"datail": "success deleted."}