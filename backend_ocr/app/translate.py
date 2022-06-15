import imp
import json
from re import L
from socket import PACKET_BROADCAST
import cv2
from PIL import Image
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



def collect_text_box():
    with open('./output/result.json') as f:
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
    
    # print(bounding_box)  
    return bounding_box         
                        
def draw_bound_box(bounding_box):
    """
    x1,y1-------------------|
    |                       |   
    |                       |
    |                       |
    |                       |
    |-------------------x2,y2
    """
    im = cv2.imread('test1.jpg',-1)
    for i in range(len(bounding_box)):
        
        x1=int(bounding_box[str(i)]['coordinate']['min_x'])
        y1=int(bounding_box[str(i)]['coordinate']['min_y'])
        x2=int(bounding_box[str(i)]['coordinate']['max_x'])
        y2=int(bounding_box[str(i)]['coordinate']['max_y'])
        
        cv2.rectangle(im,(x1,y1),(x2,y2),(0,255,0),3)
    cv2.imwrite('output/te.jpg',im)
   

def en2vi(in_dir="./output/en_text.json",out_dir="./output/vi_text.json"):
    pass

def render(in_json_dir="./output/vi_text,json", in_img_dir ="./output/0_inpainting.png",out_img_dir="./output/0_render.png"):
    pass




if __name__=="__main__":
    bounding_box =create_big_box()
    with open("output/mask_coordinate.json", "w") as f:
        json.dump(bounding_box, f)

    draw_bound_box(bounding_box)


    
        