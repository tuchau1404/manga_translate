import requests
import streamlit as st 
from PIL import Image
from io import BytesIO
#Local Environment
BACKEND_OCR_URL = "http://127.0.0.1:8000"
BACKEND_INPAINTING_URL= "http://127.0.0.1:3000"
#Docker Environment

def post_img(url:str, data):
    file = {'file': data}
    resp = requests.post(url=url, files=file) 
    return resp

def post_imgs(url:str,data1,data2):
    files= [('files', data1), ('files', data2)]
    resp = requests.post(url=url, files=files)
    return resp
def upsize(im):
    width,height = im.size
    im = im.resize((width,height))
    return im

def run():
    
    st.title("Manga Translator (EN2VN)")
    check_original = st.checkbox('Show original image',value=True)
    check_bb =st.checkbox('Show bounding box')
    check_mask = st.checkbox('Show mask image')
    check_inpainting =st.checkbox('Show inpainting image')
    check_translate =st.checkbox('Show translated image',value=True)

    im = st.file_uploader("Select an image",type=['png','jpg'])
    if im is not None:
        #resize and predict_bb
        with st.spinner("Wait for ocr..."):
            resp_predict = post_img(BACKEND_OCR_URL+"/predict",im.getvalue())
        im_predict = Image.open(BytesIO(resp_predict.content))
        if check_original:
            st.image(upsize(im_predict), caption="resized image")
        with open("./input/0.png","wb") as f:
            f.write(resp_predict.content)
        #draw bounding box
        resp_draw = requests.get(BACKEND_OCR_URL+"/draw_bb")
        im_draw = Image.open(BytesIO(resp_draw.content))
        if check_bb:
            st.image(upsize(im_draw), caption="Bouding box")
        #mask
        with st.spinner("Wait for mask..."):
            resp_mask = post_img(BACKEND_OCR_URL+"/create_mask",resp_predict.content)
        im_mask = Image.open(BytesIO(resp_mask.content))
        if check_mask:
            st.image(upsize(im_mask), caption="Mask")
        with open("./input/0_mask.png","wb") as f:
            f.write(resp_mask.content)
        #inpainting
        with st.spinner("Wait for inpainting..."):
            resp_inpainting = post_imgs(BACKEND_INPAINTING_URL+"/inpainting",open("./input/0.png","rb"),open("./input/0_mask.png","rb"))
        im_inpainting= Image.open(BytesIO(resp_inpainting.content))
        if check_inpainting:
            st.image(upsize(im_inpainting), caption="Inpainting")
        with open("./input/0_inpainting.png","wb") as f:
            f.write(resp_inpainting.content)
        #text_rendering
        with st.spinner("Wait for text rendering..."):
            resp_text_rendering = post_img(BACKEND_OCR_URL+"/text_rendering",open("./input/0_inpainting.png","rb"))
        im_text_renderring= Image.open(BytesIO(resp_text_rendering.content))
        if check_translate:
            st.image(im_text_renderring, caption="Text rendering")

if __name__ =="__main__":
    run()