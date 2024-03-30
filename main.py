import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

code_storage = {}
connections = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/share")
async def share_code(code: str):
    share_id = str(uuid.uuid4())
    code_storage[share_id] = code
    share_url = f"http://localhost:8000/view/{share_id}"
    return JSONResponse({"share_id": share_id, "share_url": share_url})

@app.get("/view/{share_id}")
async def view_shared_code(share_id: str):
    code = code_storage.get(share_id)
    if code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return {"code": code}
