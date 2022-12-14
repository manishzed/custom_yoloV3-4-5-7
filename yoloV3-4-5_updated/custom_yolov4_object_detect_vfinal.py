# -*- coding: utf-8 -*-
"""custom_yolov4_object_detect_vfinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VOROhhmM9tyFaFRWayIYvgAJaZGETW_n
"""

#refernce:
#https://medium.com/analytics-vidhya/train-a-custom-yolov4-object-detector-using-google-colab-61a659d4868


!pip install opendatasets

import opendatasets as od 
import pandas as pd

"""
Step 1:  download custom dataset annotted :

Using below kaggle API :
{"username":"softwebdatascience","key":"24a3158b65decaa911d9510581b396b5"}
"""
od.download("https://www.kaggle.com/datasets/techzizou/labeled-mask-dataset-yolo-darknet")

# Commented out IPython magic to ensure Python compatibility.
"""
Step -2 : Create & upload the following files which we need for training a custom detector

a. Labeled Custom Dataset

b. Custom cfg file

c. obj.data and obj.names files

d. process.py file (to create train.txt and test.txt files for training)

Note:  working with 2 classes i.e. with_mask and without_mask


All above file will get from below repo:

Cmd: 
"""
!git clone https://github.com/techzizou/yolov4-custom_Training.git

!cp -r /content/yolov4-custom_Training/yolov4 ./
# %cd /content/yolov4

# Commented out IPython magic to ensure Python compatibility.
#Step- 3 : Clone darknet git repository 

!git clone https://github.com/AlexeyAB/darknet

# change makefile to have GPU and OPENCV enabled
# also set CUDNN, CUDNN_HALF and LIBSO to 1

# %cd darknet/
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
!sed -i 's/LIBSO=0/LIBSO=1/' Makefile


# build darknet 
!make

!ls

# Commented out IPython magic to ensure Python compatibility.
#Step 4: Copy all the files from the yolov4 folder to the darknet directory :

# Clean the data and cfg folders first except the labels folder in data which is required
# Clean the data and cfg folders first except the labels folder in data which is required

# %cd data/
!find -maxdepth 1 -type f -exec rm -rf {} \;
# %cd ..

# %rm -rf cfg/
# %mkdir cfg

# Unzip the obj.zip dataset and its contents so that they are now in /darknet/data/ folder
#!unzip /mydrive/yolov4/obj.zip -d data/
!cp -r /content/labeled-mask-dataset-yolo-darknet/obj data



# Copy the yolov4-custom.cfg file so that it is now in /darknet/cfg/ folder 

!cp -r /content/yolov4/yolov4-custom.cfg cfg

# verify if your custom file is in cfg folder
!ls cfg/

# Copy the obj.names and obj.data files so that they are now in /darknet/data/ folder

!cp /content/yolov4/obj.names data
!cp /content/yolov4/obj.data  data


# Copy the process.py file to the current darknet directory 

!cp -r /content/yolov4/process.py .

!ls

#Step 5: Run the process.py python script to create the train.txt & test.txt files inside the data folder :


# run process.py ( this creates the train.txt and test.txt files in our darknet/data folder )
!python process.py

# list the contents of data folder to check if the train.txt and test.txt files have been created 
!ls data/



#Step 6:  Download the pre-trained yolov4 weights:


# Download the yolov4 pre-trained weights file
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137

#Step 7: Train your custom detector:

#For best results, you should stop the training when the average loss is less than 0.05 if possible or at least below 0.3, else train the model until the average loss does not show any significant change for a while.



# train your custom detector! (uncomment %%capture below if you run into memory issues or your Colab is crashing)
# %%capture


!./darknet detector train data/obj.data cfg/yolov4-custom.cfg yolov4.conv.137 -dont_show -map

!ls

