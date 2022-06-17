from paddle import scale
from paddleocr import PaddleOCR
import json
from PIL import Image,ImageOps,ImageFilter
from os import listdir
from os.path import splitext,join
import cv2
def resize(in_dir="./input/",out_dir="./output/"):
    """
    resize and convert images to png format
    """
    size = (1440,2016)
    target = '.png'
    list_dir = listdir(in_dir)
    index=0
    for file in list_dir:
        filename, extension = splitext(file)
        try:
            if extension not in ['.py','.no']:
                im = Image.open(join(in_dir,filename + extension))
                width,height=im.size
                scale = 2016/height
                print(scale)
                im = im.resize((int(width*scale),int(height*scale)))
    
                im.thumbnail(size, Image.ANTIALIAS)
                print(im.size)
                im.save(join(out_dir,str(index) + target))
                index+=1
        except OSError:
            print('Cannot convert %s' % file)

def predict(in_dir="./output/0.png",out_dir="./output/result.json"):  
    det_dir = "./models/en_PP-OCRv3_det_infer/"  
    rec_dir = "./models/en_PP-OCRv3_rec_infer/"
    ocr = PaddleOCR(use_angle_cls=False,lang='en',det_model_dir=det_dir,rec_model_dir=rec_dir)
    result = ocr.ocr(in_dir, cls=True)
    # print(result[0][1][0])
    dict = {}
    for i in range(len(result)):
        dict[i]={}
        dict[i]['det']={}
        for j in range(1,5):
            dict[i]['det'][j]={}
            dict[i]['det'][j]['x']=str(int(result[i][0][j-1][0]))
            dict[i]['det'][j]['y']=str(int(result[i][0][j-1][1]))
        dict[i]['rec']={}
        dict[i]['rec']['text']=result[i][1][0]
        dict[i]['rec']['confidence']=str(result[i][1][1])

    with open(out_dir, "w") as f:
        json.dump(dict, f)

def draw_bound_box(in_json_dir="./output/result.json",in_img_dir="./output/0.png",out_dir="./output/0_bb.png"):
    """
    x1,y1-------------------|
    |                       |   
    |                       |
    |                       |
    |                       |
    |-------------------x2,y2
    """
    with open(in_json_dir) as f:
        data = json.load(f)
    im = cv2.imread(in_img_dir)
    for index in range(len(data)):
        index = str(index)
        x1=int(data[index]['det']['1']['x'])
        y1=int(data[index]['det']['1']['y'])
        x2=int(data[index]['det']['2']['x'])
        y2=int(data[index]['det']['3']['y'])
        cv2.rectangle(im,(x1,y1),(x2,y2),(0,0,255),1)
    cv2.imwrite(out_dir,im)

#mask
"""
Ox-->
y
↓       x1,y1------------------------ x2,y2
        |                               |
        |                               |
        |                               |
        |                               |
        |                               |
        x4,y4------------------------ x3,y3
"""
def create_mask(in_dir="./input/0.png",out_dir="./output/0_mask.png", json_dir="./output/result.json"):
    with open(json_dir) as f:
        data = json.load(f)
    origin_im = Image.open(in_dir)
    width= origin_im.size[0]
    height= origin_im.size[1]
    blank_im = Image.new('RGB', (width, height),(255,255,255))
    for index in range(len(data)):
        index = str(index)
        min_y= int(data[index]["det"]["1"]["y"])
        min_x= int(data[index]["det"]["1"]["x"])
        max_x= int(data[index]["det"]["3"]["x"])
        max_y= int(data[index]["det"]["3"]["y"])
        #needs to be improved
        min_x = min(min_x,max_x)
        max_x = max(max_x,min_x)
        min_y = min(min_y,max_y)
        max_y = max(max_y,min_y)
        crop_im = origin_im.crop((min_x,min_y,max_x,max_y))
        
        blank_im.paste(crop_im,(min_x, min_y))
    #convert to black and white image
   
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    blank_im = blank_im.convert('L').point(fn, mode='1')
    blank_im = ImageOps.invert(blank_im)
    
    blank_im =blank_im.filter(ImageFilter.BLUR)
    blank_im.save(out_dir)

if __name__ == "__main__":
    create_mask()