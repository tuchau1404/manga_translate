import sndhdr
from googletrans import Translator
import json
import wordninja
from wand.image import Image
from wand.font import Font
"""
          min_y
            |
            |
            |
min_x-------|-----------max_x
            |
            |
            |
          max_y
"""

def take(index,data):
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


    x1=int(data[index]['det']['1']['x'])
    x2=int(data[index]['det']['2']['x'])
    x3=int(data[index]['det']['3']['x'])
    x4=int(data[index]['det']['4']['x'])
    y1=int(data[index]['det']['1']['y'])
    y2=int(data[index]['det']['2']['y'])
    y3=int(data[index]['det']['3']['y'])
    y4=int(data[index]['det']['4']['y'])
    return [x1,y1,x2,y2,x3,y3,x4,y4]



def collect_text_box(in_dir="./output/result.json",out_dir="./output/en_text.json"):
    with open(in_dir) as f:
        data = json.load(f)
    bounding_box ={}
    bounding_box["0"]={}
    bounding_box["0"]['sentence']=[data['0']['rec']['text']]
    bounding_box["0"]['coordinate']={}
    bounding_box["0"]['coordinate']['min_x']=data["0"]['det']['1']['x']
    bounding_box["0"]['coordinate']['max_x']= data["0"]['det']['2']['x']
    bounding_box["0"]['coordinate']['min_y']=data["0"]['det']['1']['y']
    bounding_box["0"]['coordinate']['max_y']=data["0"]['det']['3']['y']
    for i in range(1,len(data)):
        check_ok= False
        xy =take(str(i),data)
        for j in range(0,len(bounding_box)):
            check_x=False
            min_x= int(bounding_box[str(j)]['coordinate']['min_x'])
            max_x= int(bounding_box[str(j)]['coordinate']['max_x'])
            min_y= int(bounding_box[str(j)]['coordinate']['min_y'])
            max_y= int(bounding_box[str(j)]['coordinate']['max_y'])
            for x in range(0,len(xy),2):
                if min_x <= xy[x] and xy[x]<= max_x:       
                    check_x = True
            if xy[0]<=min_x and min_x<=xy[2]:
                check_x=True
            if xy[0]<=max_x and max_x<=xy[2]:
                check_x=True
            if check_x ==True:
                max_distance=0.3*(max_y-min_y)
                y3= xy[5]
                y1= xy[1]
                
                if abs(max_y-y1)<=max_distance or abs(min_y-y3)<=max_distance:
                    text = bounding_box[str(j)]['sentence']
                    text.append(data[str(i)]['rec']['text'])
                    bounding_box[str(j)]['sentence'] = text
                    bounding_box[str(j)]['coordinate']['min_x']=min(min_x,xy[0],xy[2],xy[4],xy[6])
                    bounding_box[str(j)]['coordinate']['max_x']=max(max_x,xy[0],xy[2],xy[4],xy[6])
                    bounding_box[str(j)]['coordinate']['min_y']=min(min_y,xy[1],xy[3],xy[5],xy[7])
                    bounding_box[str(j)]['coordinate']['max_y']=max(min_y,xy[1],xy[3],xy[5],xy[7])
                    check_ok = True
                    break
        if check_ok ==False:
            index = str(len(bounding_box))
            bounding_box[index]={}
            bounding_box[index]['sentence']= [data[str(i)]['rec']['text']]
            bounding_box[index]['coordinate']={}
            bounding_box[index]['coordinate']['min_x']=min(xy[0],xy[2],xy[4],xy[6])
            bounding_box[index]['coordinate']['max_x']=max(xy[0],xy[2],xy[4],xy[6])
            bounding_box[index]['coordinate']['min_y']=min(xy[1],xy[3],xy[5],xy[7])
            bounding_box[index]['coordinate']['max_y']=max(xy[1],xy[3],xy[5],xy[7])
    with open(out_dir, "w") as f:
        json.dump(bounding_box, f) 

def en2vi(in_dir="./output/en_text.json",out_dir="./output/vi_text.json"):
    with open(in_dir) as f:
        data = json.load(f)
    translator = Translator()
    for index in range(0,len(data)):
        sentence=""
        index =str(index)
        word_list = data[index]["sentence"]
        for word in word_list:
            word =word.replace("-","")
            sentence+=word
        # wordnija : fix missing spaces
        word_list = wordninja.split(sentence)
        sentence=""
        for word in word_list:
            sentence=sentence + word+" "
        vi_sentence = translator.translate(sentence,dest="vi",src="en")
        data[index]["sentence"] = vi_sentence.text
    with open(out_dir, "w",encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False) 
    

def render(in_json_dir="./output/vi_text.json", in_img_dir ="./input/0_inpainting.png",out_img_dir="./output/0_render.png",scale=3):
    with open(in_json_dir) as f:
        data = json.load(f)
    with Image(filename=in_img_dir) as canvas:
        size = canvas.size
        canvas.resize(size[0]*scale,size[1]*scale)
        for index in range(len(data)):
            index =str(index)
            left =int(data[index]["coordinate"]["min_x"])*scale
            top  =int(data[index]["coordinate"]["min_y"])*scale
            width= (int(data[index]["coordinate"]["max_x"])-int(data[index]["coordinate"]["min_x"]))*scale
            height= (int(data[index]["coordinate"]["max_y"])- int(data[index]["coordinate"]["min_y"]))*scale
            sentence= data[index]["sentence"]
            font =Font("./fonts/000_10_Cent_Comics_[TeddyBear].ttf")
            canvas.caption(sentence,left=left,top=top,width=width,height=height,font=font,gravity="center",)
        canvas.resize(size[0],size[1])
        canvas.save(filename=out_img_dir)
            

            





if __name__=="__main__":
    collect_text_box()
    en2vi()


    
        