from turtle import color
import cv2
import torch
import os

import torch.multiprocessing
import sys

if __name__ == "__main__":    

    # 打印 sys.maxsize 的值
    print("sys.maxsize:", sys.maxsize)
    
    
    filename = "/home/yolo/YOLOv4/data/img/1_125016_00.jpg"
    parts = filename.split('_')
    #id = int(parts[-1][0:-4])	//Larry modify
    #ascii_ids = ord(parts[0][-1])

    ascii_ids = ord(parts[0].split("/")[-1])
    print(ascii_ids)

    strID = chr(ascii_ids) + parts[1] + parts[-1].lower().replace(".jpg", "")
    print("Pic ID=" + strID)
    
    
    #img_path = '/home/yolo/YOLOv4/data/img/1_110636_00.jpg\n'                
    img_path = '/home/yolo/YOLOv4/data/img/1_110636_00.jpg'

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #db6923

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    num_gpus = torch.cuda.device_count()
    print("GPU Count: ", num_gpus)