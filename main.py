from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from model import QueryParams
from responseClass import Metadata, ApiResponse
from scripts.main import query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://110.42.179.122:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./front/static"), name="static")

@app.get("/index")
async def read_index():
    return FileResponse('./front/index.html')

@app.post("/api/list")
def list(body: QueryParams):
    try:
        print("接收到请求")
        entries = query(body.regions, body.keyword1, body.type1, body.keyword2, body.type2, body.radius)
        entries_dict = [entry.to_dict() for entry in entries]
        metadata = Metadata(code='ok', message='Success')
        response = ApiResponse(metadata=metadata, result=entries_dict)
        return response
    except Exception as e:
        error_metadata = Metadata(code='err', message=str(e))
        error_response = ApiResponse(metadata=error_metadata)
        return error_response

@app.get("/hello")
def hello():
    return {"message": "Hello World"}