from paddleocr import PaddleOCR
import json
from PIL import Image
from os import listdir
from os.path import splitext,join

def resize(target_dir,out_dir="output/resize_imgs"):
    """
    resize and convert images to png format
    """
    size = (600,840)
    target = '.png'
    list_dir = listdir(target_dir)
    index=0
    for file in list_dir:
        filename, extension = splitext(file)
        try:
            if extension not in ['.py','.no']:
                print(extension)
                im = Image.open(join(target_dir,filename + extension))
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(join(out_dir,str(index) + target))
                index+=1
        except OSError:
            print('Cannot convert %s' % file)

def predict_path(img_path):  
    det_dir = "ocr/models/en_PP-OCRv3_det_infer/"  
    rec_dir = "ocr/models/en_PP-OCRv3_rec_infer/"
    ocr = PaddleOCR(use_angle_cls=False,lang='en',det_model_dir=det_dir,rec_model_dir=rec_dir)
    result = ocr.ocr(img_path, cls=True)
    # print(result[0][1][0])
    dict = {}
    for i, line in enumerate(result):
        dict[i]={}
        dict[i]['det']={}
        for j in range(1,5):
            dict[i]['det'][j]={}
            dict[i]['det'][j]['x']=str(int(result[i][0][j-1][0]))
            dict[i]['det'][j]['y']=str(int(result[i][0][j-1][1]))
        dict[i]['rec']={}
        dict[i]['rec']['text']=result[i][1][0]
        dict[i]['rec']['confidence']=str(result[i][1][1])

    with open("output/result.json", "w") as f:
        json.dump(dict, f)

if __name__ == "__main__":
    resize(target_dir="assets/img_exam")
    # predict_path("output/img_resize.jpg")
  