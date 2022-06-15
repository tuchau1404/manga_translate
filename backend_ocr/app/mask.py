#inpainting
from PIL import Image,ImageOps,ImageFilter
import json
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
def create_mask(in_dir,out_dir="output/blank.png", json_dir="output/result.json"):

    with open(json_dir) as f:
        data = json.load(f)
    origin_im = Image.open(in_dir)
    n= origin_im.size[0]
    m= origin_im.size[1]
    blank_im = Image.new('RGB', (n, m),(255,255,255))
    for i in range(len(data)):
        min_y= int(data[str(i)]["det"]["1"]["y"])
        min_x= int(data[str(i)]["det"]["1"]["x"])
        max_x= int(data[str(i)]["det"]["3"]["x"])
        max_y= int(data[str(i)]["det"]["3"]["y"])
        crop_im = origin_im.crop((min_x,min_y,max_x,max_y))
        blank_im.paste(crop_im,(min_x, min_y))
    #convert to black and white image
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    blank_im = blank_im.convert('L').point(fn, mode='1')
    blank_im = ImageOps.invert(blank_im)
    blank_im =blank_im.filter(ImageFilter.BLUR)
    blank_im.save(out_dir)

if __name__ =="__main__":
    run(in_dir="output/resize_imgs/0.png",out_dir="output/resize_imgs/0_mask1.png")
