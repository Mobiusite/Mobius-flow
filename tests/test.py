import os
import json
import hashlib
from collections import defaultdict

# 定义一个函数，用来计算文件的MD5码
def get_md5(file_path):
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()
    except Exception as e:
        print(f'Error: {e}')
        return None

# 定义一个函数，用来遍历目录并生成字典a
def get_dict(dir_path):
    # 初始化字典a，使用defaultdict()函数，指定默认值为字典或列表
    a = defaultdict(dict)
    a['file'] = defaultdict(str)
    a['dir'] = defaultdict(dict)
    # 遍历目录下的所有文件和文件夹
    for entry in os.scandir(dir_path):
        # 如果是文件，就获取文件名和MD5码，并添加到字典a的file键对应的字典c中
        if entry.is_file():
            file_name = entry.name
            file_path = entry.path
            file_md5 = get_md5(file_path)
            if file_md5:
                a['file'][file_name] = file_md5
        # 如果是文件夹，就获取子目录路径，并添加到字典a的dir键对应的列表a中，并递归调用函数，获取子目录下的所有文件和文件夹，并添加到字典a的dir键对应的字典b中
        elif entry.is_dir():
            sub_dir = entry.path
            a['dir'][sub_dir] = get_dict(sub_dir)
    # 返回字典a，使用dict()函数转换为普通字典
    return dict(a)

# 测试代码，假设要遍历的目录是test
dir_path = '/home'
a = get_dict(dir_path)
formatted_a = json.dumps(a, indent=4)
print(formatted_a)