#!/usr/bin/env python
# Martin Kersner, m.kersner@gmail.com
# 2016/01/18

import numpy as np

def pascal_classes():
  '''
  classes name and id table
  '''
  classes = {'benign': 1,  'malignant': 2}

  return classes

def pascal_palette():
  '''
  pascal voc rgb and classes id table
  '''
  palette = {(  0,   0,   0) : 0 ,
             (  0, 128,   0) : 1 ,
             (  0,   0, 128) : 2}

  return palette

def convert_from_color_segmentation(arr_3d):
  '''
  convert pascal voc bgr to gray scale as clases index

  arguments:
    arr_3d: rgb image
  '''
  arr_2d = np.zeros((arr_3d.shape[0], arr_3d.shape[1]), dtype=np.uint8)
  palette = pascal_palette()

  # slow!
  print(arr_3d.shape)
  for i in range(0, arr_3d.shape[0]):
    for j in range(0, arr_3d.shape[1]):
      # each channel's tuple is key of rgb and index table
      key = (arr_3d[i,j,0], arr_3d[i,j,1], arr_3d[i,j,2])
      arr_2d[i, j] = palette.get(key, 0) # default value if key was not found is 0

  return arr_2d

def get_id_classes(classes):
  '''
  get index of class name
  arguments:
    classes: array of class names
  '''
  all_classes = pascal_classes()
  id_classes = [all_classes[c] for c in classes]
  return id_classes

def strstr(str1, str2):
  '''
  if str1 include str2 as sub set, return True
  '''
  if str1.find(str2) != -1:
    return True
  else:
    return False


if __name__ == '__main__':
  print "['bus', 'car'] --->"
  print get_id_classes(['bus', 'car'])
