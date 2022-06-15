#uvicorn app.main:app --port 3000 --reload
from typing import List
from fastapi import File, UploadFile, FastAPI
from fastapi.responses import FileResponse
import os, subprocess
app = FastAPI()
    
@app.post("/inpainting")
async def upload(files: List[UploadFile] = File(...)):
    file_dir_list=[]
    for file in files:
        try:
            contents = await file.read()
            file_dir= os.path.join("./input",file.filename)
           
            file_dir_list.append(file_dir)
            with open(file_dir, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            await file.close() 
    subprocess.run("./app/inpainting.sh")       
    #remove files in folder input
    for dir in file_dir_list:
        os.remove(dir)
    return FileResponse(path ="./output/0_mask.png")
        
    