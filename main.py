from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from con_sql import *

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://192.168.100.7:8000",  # replace with your LAN IP
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,       # allow only these origins
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)


# Mount static folder for JS/CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/clients")
def validate_key_endpoint():
    clients = get_clients() 
    return {"status": "success", "clients": clients}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
