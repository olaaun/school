#This is used for adding color coding to the annotations
#Separating between malignant (blue) and benign (green) tumors
#Also resizes pictures to save memory

import glob
from PIL import Image
import math
import PIL


def alter_annotation(image, tumor_type, filename):
    color = (0,0,128) if tumor_type=="Malignantall" else (0,128,0)
    copy = Image.new("RGB", image.size)
    copy.putdata(map(
                  lambda pixel: color if pixel>1 else (0,0,0),
                  image.getdata()
                 )
             )
    basewidth = 500
    wpercent = (basewidth/float(copy.size[0]))
    hsize = int((float(copy.size[1])*float(wpercent)))
    copy = copy.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    copy.save('labels/' + filename.replace("_anno",""))


base_path = "colon_training_dataset/Colon Training Dataset/"
for tumor_type in ["Malignantall", "Benignall"]:
    for filename in glob.glob(base_path+tumor_type+"/annotation/*.bmp"):
        i = Image.open(filename)
        alter_annotation(i, tumor_type, filename.split("/")[-1])
