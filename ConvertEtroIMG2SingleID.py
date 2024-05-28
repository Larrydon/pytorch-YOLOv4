import datetime
import sys
import os
import fnmatch
import re
import shutil
from datetime import datetime

from numpy import imag


#from tkinter import Y
#from torch import true_divide

# ConvertEtroIMG2SingleID
# 將 Etro產品的圖檔命名規則改至單一檔案上，用檔名來當作唯一值，才能夠提供給圖檔 index
# 年/月/日/車格名稱/車格名稱_時間_第幾張.jpg
# /home/yolo/IMG/FREEWAY/Hukou_North/2024/04/07/E39/E39_010145_00.jpg


# 檢查是否提供了足夠的參數
# 帶入的第一個參數<圖檔路徑> 必須是ETRO分層的有時間分隔開的資料夾
if len(sys.argv) < 3:
    print("Usage: python ConvertEtroIMG2SingleID.py <IMG path> <Save path for convert>")
    sys.exit(1)

source_img_path = sys.argv[1]
convert2singleid_path = sys.argv[2]


def find_images(source):
    # 用於匹配的圖檔擴展名
    # patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
    patterns = ['*.jpg', '*.jpeg']
    
    # 用於存儲結果的清單
    image_files = []

    # 遍歷目錄樹
    for root, dirs, files in os.walk(source):
        # 檢查每個文件是否匹配圖檔擴展名
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                # 如果匹配，則加入清單
                image_files.append(os.path.join(root, filename))
            
    
    return image_files


# 找出所有圖檔
images = find_images(source_img_path)

## 輸出結果
#for image in images:
#    print(image)

def CheckAllIsNumber(input_text)->bool:
    if re.fullmatch(r'\d+', input_text):
        return True
    else:
        return False
    


def copy_and_rename_file(src_file_path, dest_dir, new_file_name):
    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # 组合新的文件路径
    dest_file_path = os.path.join(dest_dir, new_file_name)
    
    # 复制并重命名文件
    shutil.copy(src_file_path, dest_file_path)
    print(f"原始文件: {src_file_path}")
    print(f"文件已复制并重命名为: {dest_file_path}")
    
    
def is_alphanumeric(char):
    """
    判斷一個字元是否只包含英文字母或數字。
    
    參數:
    char (str) - 要檢查的字元
    
    返回:
    bool - 如果字元只包含英文字母或數字,返回 True,否則返回 False
    """
    pattern = r'^[a-zA-Z0-9]$'
    if re.match(pattern, char):
        return True
    else:
        return False


try:
    i = 0
    now = datetime.now()
    for image in images:
        i += 1
        # >2024-05-22 Larry Add 
        # 由於int會爆，因此原本打算 拿車格號轉ASCII+時間年月日+序號 會無法使用，故棄用了
        # 
        # ls = image.split("/")
        # year = ""
        # month = ""
        # day = ""
        # space_name = ""
        # for i in range(-2, -6, -1):
        #     if i < -2:
        #         if not CheckAllIsNumber(ls[i]):
        #             ("Folder name is not all of number:", ls[i])
        #             exit
        # 
        #     if i == -2:
        #         space_name = ls[i]
        #     elif i == -3:
        #         day = ls[i]
        #     elif i == -4:
        #         month = ls[i]
        #     else:
        #         year = ls[i]
        #         dest_singleID = (year + month + day + ls[-1].replace(space_name, "")).replace("_", "")
        #         # 用于存储ASCII码的列表
        #         ascii_list = []
        # 
        #         # 遍历字符串中的每个字符
        #         for char in space_name:
        #             # 检查字符是否是字母或数字
        #             if is_alphanumeric(char):
        #                 # 将字符转换为ASCII码并添加到列表中
        #                 ascii_list.append(ord(char))
        #         #print("字符串的ASCII码列表:", ascii_list)
        # 
        #         dest_singleID = ''.join(str(x) for x in ascii_list) + dest_singleID
        #         copy_and_rename_file(image, convert2singleid_path, dest_singleID)
        # <End
        

        # 直接更名為現在時間加上4碼流水序號產生(一天的照片最多會到上千筆圖檔)    
        # 使用 os.path.splitext 分割路径和扩展名
        file_name, file_extension = os.path.splitext(image)    
        dest_singleID = now.strftime("%Y%m%d%H%M%S") + f"{i:04}" + file_extension
        copy_and_rename_file(image, convert2singleid_path, dest_singleID)
        print(dest_singleID)
                
except Exception as e:
    print("Error:", e)
    
    

