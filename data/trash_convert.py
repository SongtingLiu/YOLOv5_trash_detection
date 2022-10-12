import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
names = {
    "cardboard": 0,
    "glass": 1,
    "metal": 2,
    "paper": 0,
    "plastic": 3,
}


def convert_box(size, box):
    dw, dh = 1. / size[0], 1. / size[1]
    x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh
def convert_whole_folder(label_path, label_file_names):
    for f in label_file_names:
        in_file_name = path+label_path+'/'+f
        in_file = open(in_file_name)
        out_file = open(in_file_name.replace(".xml", ".txt"),'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find("size")
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls in list(names.keys()):
                xmlbox = obj.find('bndbox')
                bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])
                cls_id = names[cls]  # class id
                out_file.write(" ".join([str(a) for a in (cls_id, *bb)]) + '\n')
# convert Trash dataset labels from xml to YOLO format
path = "D:/datasets/Trash/"
train_image_path = "train/images"
val_image_path = "val/images"

# get label path by replacing "images" by "labels"
train_label_path = train_image_path.replace("images", "labels")
val_label_path = val_image_path.replace("images", "labels")

# get train label file names
for i, j, k in os.walk(path+train_label_path):
    label_file_names = k
convert_whole_folder(train_label_path, label_file_names)

# get valid label file names
for i, j, k in os.walk(path+val_label_path):
    label_file_names = k
convert_whole_folder(val_label_path, label_file_names)
