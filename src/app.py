from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.database import insert_solicitud
app = FastAPI()

@app.post('/solicitud')
def solicitud(request: Request):
    data = request.body
    result = insert_solicitud(data)
    return JSONResponse(content=result, status_code=200)