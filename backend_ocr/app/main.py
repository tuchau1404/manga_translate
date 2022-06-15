#uvicorn app.main:app --reload
from typing import List
from fastapi import File, UploadFile, FastAPI
from fastapi.responses import FileResponse
import os, subprocess
app = FastAPI()
    
@app.post("/predict")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    return FileResponse(path ="./output/0.png")

@app.post("/predict")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    return FileResponse(path ="./output/0.png")
        
@app.post("/predict")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    return FileResponse(path ="./output/0.png")
        

        
    