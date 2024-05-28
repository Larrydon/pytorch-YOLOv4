import os
import sys
from tool import darknet2pytorch
import torch


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 檢查是否提供了足夠的參數
# 
if len(sys.argv) < 4:
    print("Usage: python weight2pth.py <IN .cfg> <IN .weights> <OUT .pth>")
    sys.exit(1)

# 提取命令行引數
config_file = _BASE_DIR + sys.argv[1]   # './cfg/yolov4.cfg'
weights_file = _BASE_DIR + sys.argv[2]  # './weight/yolov4.weights'
pth_file = _BASE_DIR + sys.argv[3]  # './weight/yolov4-pytorch.pth'

# 遍歷命令行引數列表，從第二個元素開始
print("Arguments:")
for arg in sys.argv[1:]:
    print(arg)


model = darknet2pytorch.Darknet(config_file, inference=True)
model.load_weights(weights_file)

torch.save(model.state_dict(), pth_file)

print("Save complete. <" + pth_file + ">")