from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="./", html=True), name="static")

@app.get("/solicitud")
def read_solicitud():
    return {"message": "Solicitud"}

@app.get("/solicitudes")
def read_solicitudes():
    return {"message": "Solicitudes"}