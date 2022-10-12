import argparse
import os
import platform
import sys
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


class Pi_Detector():
    def __init__(self,
                 weights=ROOT / 'yolov5s_combined_trash.pt',
                 data=ROOT / 'data/coco128.yaml',
                 imgsz=(640, 640),
                 conf_thres=0.25,
                 iou_thres=0.45,
                 max_det=1000,
                 device='cpu'):
        # load model weights
        self.device = select_device(device)
        self.model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=False)
        self.stride, names, pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        self.model.warmup(imgsz=(1, 3, *self.imgsz))  # warmup
        self.conf_thres=0.25
        self.iou_thres=0.45
        self.max_det=1000
        self.seen, self.windows, self.dt = 0, [], (Profile(), Profile(), Profile())

    def detect(self, im):
        with self.dt[0]:
            im = torch.from_numpy(im).to(self.device)
            im = im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
        with self.dt[1]:
            pred = self.model(im, augment=False, visualize=False)

        with self.dt[2]:
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, None, False, max_det=self.max_det)

        return pred





