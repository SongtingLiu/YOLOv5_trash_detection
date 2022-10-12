# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:31:02 2022

@author: lenovo
"""

import shutil
import os
import numpy as np
import glob

# 0: glass
# 1: metal
# 2: plastic

# Trashnet path
trashnet_path = "D:/datasets/Trash"

# 4 -> 0
# 1 -> 2
# 2 -> 1

label_list = glob.glob(os.path.join(trashnet_path, "*", "*", "plastic*.txt"))
for f in label_list:
    data = np.loadtxt(f)
    if len(data):
        data = np.expand_dims(data, axis=0) if data.ndim == 1 else data
        data[:, 0] = 2
    outfile = open(f, 'w')
    for i in range(data.shape[0]):
        outfile.write(" ".join([str(a) for a in data[i, :]]) + '\n')
    outfile.close()

label_list = glob.glob(os.path.join(trashnet_path, "*", "*", "glass*.txt"))
for f in label_list:
    data = np.loadtxt(f)
    if len(data):
        data = np.expand_dims(data, axis=0) if data.ndim == 1 else data
        data[:, 0] = 0
    outfile = open(f, 'w')
    for i in range(data.shape[0]):
        outfile.write(" ".join([str(a) for a in data[i, :]]) + '\n')
    outfile.close()
    
label_list = glob.glob(os.path.join(trashnet_path, "*", "*", "metal*.txt"))
for f in label_list:
    data = np.loadtxt(f)
    if len(data):
        data = np.expand_dims(data, axis=0) if data.ndim == 1 else data
        data[:, 0] = 1
    outfile = open(f, 'w')
    for i in range(data.shape[0]):
        outfile.write(" ".join([str(a) for a in data[i, :]]) + '\n')
    outfile.close()

dfile_list = glob.glob(os.path.join(trashnet_path, "*", "*", "cardboard*"))
for f in dfile_list:
    os.remove(f)

dfile_list = glob.glob(os.path.join(trashnet_path, "*", "*", "paper*"))
for f in dfile_list:
    os.remove(f)

# # Image_of_Waste path
# image_of_waste_path = "D:/datasets/Images_of_Waste"
#
# # AluCan -> 1
# # Glass -> 2
# # HDPEM -> 0
# # PET -> 0
#
# label_list = glob.glob(os.path.join(image_of_waste_path, "*", "AluCan*.txt"))
# for f in label_list:
#     data = np.loadtxt(f)
#     if len(data):
#         data = np.expand_dims(data, axis=0) if data.ndim==1 else data
#         data[:, 0] = 1
#     np.savetxt(f, data)
#
# label_list = glob.glob(os.path.join(image_of_waste_path, "*", "Glass*.txt"))
# for f in label_list:
#     data = np.loadtxt(f)
#     if len(data):
#         data = np.expand_dims(data, axis=0) if data.ndim==1 else data
#         data[:, 0] = 2
#     np.savetxt(f, data)
#
# label_list = glob.glob(os.path.join(image_of_waste_path, "*", "HDPEM*.txt"))
# for f in label_list:
#     data = np.loadtxt(f)
#     if len(data):
#         data = np.expand_dims(data, axis=0) if data.ndim==1 else data
#         data[:, 0] = 0
#     np.savetxt(f, data)
#
# label_list = glob.glob(os.path.join(image_of_waste_path, "*", "PET*.txt"))
# for f in label_list:
#     data = np.loadtxt(f)
#     if len(data):
#         data = np.expand_dims(data, axis=0) if data.ndim==1 else data
#         data[:, 0] = 0
#     np.savetxt(f, data)
