import uvicorn,os
if not os.path.exists("./log"):
    os.mkdir("./log")
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6789, reload=True,ssl_keyfile="localhost.key",ssl_certfile="localhost.crt")