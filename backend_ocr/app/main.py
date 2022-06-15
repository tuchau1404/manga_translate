#uvicorn app.main:app --reload

from fastapi import File, UploadFile, FastAPI
from fastapi.responses import FileResponse
import os
from app.mask import *
from app.ocr import *
from app.translate import *
app = FastAPI()
    

@app.post("/predict")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
        resize()
        predict()
        os.remove(file_dir)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    
    return FileResponse(path ="./output/0.png")

@app.get("/draw_bb")
async def upload():
    draw_bound_box()
    return FileResponse(path ="./output/0_bb.png")


@app.post("/create_mask")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
        create_mask()
        os.remove(file_dir)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    return FileResponse(path ="./output/0_mask.png")
        

@app.post("/text_rendering")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_dir= os.path.join("./input","0_inpainting.png")
        with open(file_dir, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        await file.close() 
    return FileResponse(path ="./output/0.png")
        

        
    