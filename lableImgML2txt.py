import argparse
from os import getcwd
from sklearn.model_selection import train_test_split
import json
import glob
import sys

def main():
    # 检查命令行参数数量
    if len(sys.argv) < 2:
        print("Usage: python AAA.py [arg1] [arg2] ...")
        return

    # 获取命令行参数
    args = sys.argv[1:]

    # 打印命令行参数
    print("Arguments:", args)

    # 在这里进行其他操作，根据需要处理命令行参数


if __name__ == "__main__":
    main()


wd = getcwd()
"labelme标注的json 数据集转为pytorch版yolov4的训练集"

#>2024/05/09 Larry modify
#classes = ["aircraft","oiltank"]
#image_ids = glob.glob(r"LabelmeData/*jpg")

parser = argparse.ArgumentParser(description='labelImg ML format  transfer to PyTorch YoloV4 format',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-dir', type=str, default=None, help='dataset path')
parser.add_argument('-clasessname', type=str, default=None, help='obj.names path')
args = vars(parser.parse_args())

arg_dir_path = wd + args['dir'] + "/*jpg"
arg_classname_path = wd + args['clasessname']

classes = []
with open(arg_classname_path, 'r') as file:
    for line in file:
        classes.append(line.strip())
#<End

image_ids = glob.glob(arg_dir_path)
image_ids.sort()

print(image_ids)
train_file_path = wd + '/data/train.txt'
valid_file_path = wd + '/data/valid.txt'
train_list_file = open(train_file_path, 'w')
val_list_file = open(valid_file_path, 'w')


def convert_annotation(image_id, list_file):
    jsonfile=open('%s.json' % (image_id))
    in_file = json.load(jsonfile)

    
    #for i in range(0,len(in_file["annotations"])):
    for i in range(0, len(in_file[0]["annotations"])):
        object=in_file[0]["annotations"][i]
        cls=object["label"]
        points=object["coordinates"]
        xmin = int(points['x'])
        ymin = int(points['y'])
        xmax = xmin + int(points['width'])
        ymax = ymin + int(points['height'])
        if cls not in classes:
            print("cls not in classes")
            continue
        cls_id = classes.index(cls)
        b = (xmin, ymin, xmax, ymax)
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    jsonfile.close()


def ChangeData2TXT(image_List,dataFile):
    for image_id in image_List:
        dataFile.write('%s' % (image_id.split('\\')[-1]))
        convert_annotation(image_id.split('.')[0], dataFile)
        dataFile.write('\n')
    dataFile.close()


trainval_files, test_files = train_test_split(image_ids, test_size=0.2, random_state=55)
ChangeData2TXT(trainval_files,train_list_file)
ChangeData2TXT(test_files,val_list_file)

print("Save to: %s、%s <Finish>" % (train_file_path, valid_file_path))