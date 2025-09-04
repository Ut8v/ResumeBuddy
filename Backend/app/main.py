from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def getCheck():
    return {"OK": True}
