import os

# merge Image of Waste dataset with Trashnet dataset
Trashnet_names = {
    "cardboard": 0,
    "glass": 1,
    "metal": 2,
    "paper": 3,
    "plastic": 4,
}
IoW_names = {
    "metal": 0,
    "glass": 1,
    "plastic": [2, 3],
}

# Firstly, read the path and the file names
# In this dataset, refer to label files since the number of label files is 10 less than images mysteriously
path = "D:/datasets/Images_of_Waste/"
for i, j, k in os.walk(path + "labels"):
    label_file_names = k
