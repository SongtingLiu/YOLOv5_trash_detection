import socket
import threading
import time
import sys
import os
import struct
import cv2
import numpy as np
from pi_detect import Pi_Detector
from utils.augmentations import letterbox

class Socket_Server():
    def __init__(self):
        self.detector = Pi_Detector()
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host = '0.0.0.0'
            self.s.bind((host, 8123))  # 这里换上自己的ip和端口
            self.s.listen(5)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        print("Waiting...")

    def receive_connection(self):
        self.conn, self.addr = self.s.accept()
        print('Accept new connection from {0}'.format(self.addr))

    def receive_one_data(self):
        fileinfo_size = struct.calcsize('128sl')
        buf = self.conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(str.encode('\00'))
            new_filename = os.path.join(str.encode('./') + fn)
            self.filepath = new_filename
            print('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print("start receiving...")
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = self.conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = self.conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
    def predict_one_data(self):
        # read & preprocess data
        path = self.filepath
        im0 = cv2.imread(self.filepath)
        assert im0 is not None, f'Image Not Found {self.filepath}'
        im = letterbox(im0, self.detector.imgsz, stride=self.detector.stride, auto=True)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous
        pred = self.detector.detect(im = im)
        pred = pred[0].cpu().numpy() # in shape of (x, 6) where x is the number of targets
        pred[:, :4] /= self.detector.imgsz[0] # prediction data in x1, y1, x2, y2, conf, cls sequence
        print(pred)

        return pred
    def send_prediction(self, pred):
        self.s.send(pred.reshape(-1, 1).tobytes())
    def deal_data_recurrently(self):
        while 1:
            self.receive_one_data()
            pred = self.predict_one_data()

if __name__ == "__main__":
    server = Socket_Server()
    server.receive_connection()
    server.receive_one_data()
    pred = server.predict_one_data()
    server.send_prediction(pred)

    print(pred)