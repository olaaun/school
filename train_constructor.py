import glob

#Used to create index files
#train.txt is list of data set
#benign.txt and malignan.txt contains list of images with respective classes 
f = open("train.txt", "w")
for filename in glob.glob("flat_dataset/*bmp"):
    f.write(filename.replace("flat_dataset/", "") + "\n")

f.close()

base_path ="/home/olaaun/tumor_segmentation/colon_training_dataset/Colon Training Dataset/"
f = open("benign.txt", "w")
for filename in glob.glob(base_path + "Benignall/*.bmp"):
    f.write(filename.replace(base_path+"Benignall/", "") + "\n")
f.close()
f = open("malignant.txt", "w")
for filename in glob.glob(base_path + "Malignantall/*.bmp"):
    f.write(filename.replace(base_path+"Malignantall/", "") + "\n")
f.close()
