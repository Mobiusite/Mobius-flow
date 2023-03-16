import os
import re
import shelve
import logging
import hashlib
from deepdiff import DeepDiff
from defaultlist import defaultlist

class compress:
    # TODO 增加多压缩类
    def check_out(
        self,
        dir_path:str,
        format:str
        ):
        # TODO 适配多压缩类
        """初始化并检查目标文件夹

        Args:
            dir_path (str): 目标文件夹
            format (str): 压缩格式
        """
        try:
            if format not in ['zip','7z','tar','targz','E_targz']:
                raise ValueError("format必须是以下'zip','7z','tar','targz','E_targz'值中的一个")
            else:
                self.SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), format)
                self.SNAPSHOT_FILE = os.path.join(self.SNAPSHOT_PATH, "snapshot")
                self.snapshot()
            raw_dict = self.get_dirdict(dir_path)
            if raw_dict:
                if self.diffsnapshot(raw_dict):
                    print('compress!')
                else:
                    print('waiting')
                self.snapshot(raw_dict)
        except FileNotFoundError:
            logging.error(f'file not find!')
        except ValueError:
            logging.error(f'format必须是以下zip,7z,tar,targz,E_targz值中的一个')
            
    def snapshot(
        self,
        snapshot:dict={}
        ):
        """初始化快照并将快照持久化至snapshot文件中.
        
        如果快照不存在且无对应key值则进行首次初始化,若snapshot输入空值且文件存在且包含key值,则跳过初始化.

        Args:
            snapshot (list, optional): 输入要进行快照文件列表. 默认为[]以进行初始化.
        """
        if os.path.exists(self.SNAPSHOT_PATH):
            if os.path.isfile(self.SNAPSHOT_FILE):
                new_snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
                if snapshot:
                    new_snapshot['snapshot'] = snapshot
            elif os.path.isdir(self.SNAPSHOT_FILE):
                self.rm_errordir(self.SNAPSHOT_FILE)
                os.rmdir(self.SNAPSHOT_FILE)
                new_snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
            else:
                new_snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
        else:
            os.mkdir(self.SNAPSHOT_PATH)
            new_snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
        if 'snapshot' not in new_snapshot:
            new_snapshot['snapshot'] = snapshot
        new_snapshot.close()
        
    def diffsnapshot(
        self,
        diff_snapshot:dict
        ):
        # TODO 检查目录下的子文件夹是否一致?
        raw_snapshot = shelve.open(filename=self.SNAPSHOT_FILE,writeback=True)
        if raw_snapshot['snapshot']:
            file_diff = set(
                diff_snapshot['file'].items()).difference(
                    set(raw_snapshot['snapshot']['file'].items())
                )
            self.subdir_diff = DeepDiff(
                raw_snapshot['snapshot'], 
                diff_snapshot,
                exclude_paths="root['file']"
            ).to_dict()
            raw_snapshot.close()
            file_diff_list = []
            subdir_diff_list = []
            if file_diff:
                file_diff_list = list(file_diff)
            elif self.subdir_diff:
                origin_subdir_name_list = []
                origin_subdir_name_list.append(self.get_subdir_name_list('dictionary_item_added'))
                origin_subdir_name_list.append(self.get_subdir_name_list('values_changed'))
                origin_subdir_name_list.append(self.get_subdir_name_list('iterable_item_added'))
                origin_subdir_name_list.append(self.get_subdir_name_list('iterable_item_removed'))
                subdir_diff_list = list(set(origin_subdir_name_list))
            return file_diff_list + subdir_diff_list
        else:
            file_diff_list = list(diff_snapshot['file'])
            subdir_diff_list = list(diff_snapshot['dir'])
            raw_snapshot.close()
            return file_diff_list + subdir_diff_list

    def get_md5(
        self,
        dir_path:str
        ):
        """或者指定文件的MD5码

        Args:
            dir_path (str):指定的文件路径

        Returns:
            None: 若失败则返回空值
            md5.hexdigest(): 成功则返回MD5码
        """
        md5 = hashlib.md5()
        try:
            with open(dir_path, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    md5.update(data)
            return md5.hexdigest()
        except Exception as e:
            logging.error(f'生成MD5码失败')
            return None
        
    def rm_errordir(
        self,
        remove_dir:str
        ):
        """删除目标文件夹及其内部所有文件与文件夹

        Args:
            remove_dir (str): 要删除的文件夹路径
        """
        if os.listdir(remove_dir):
            for filename in os.listdir(remove_dir):
                file_path = os.path.join(remove_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    self.rm_errordir(file_path)
                    os.rmdir(file_path)
        else:
            os.rmdir(remove_dir)
            
    def get_dirdict(
        self,
        dir_path:str
        ):
        """遍历目录并生成格式为字典的快照

        Args:
            dir_path (str): 要遍历的路径

        Returns:
            dict: 返回一个包含目录,文件名,MD5及子目录的字典
        """
        dir_dict = dict()
        dir_dict['file'] = dict()
        dir_dict['dir'] = dict()
        for entry in os.scandir(dir_path):
            if entry.is_dir():
                sub_dir_name = entry.name
                sub_dir_path = entry.path
                dir_dict['dir'][sub_dir_name] = dict()
                dir_dict['dir'][sub_dir_name]['file'] = dict()
                dir_dict['dir'][sub_dir_name]['dir'] = list()
                # os.walk遍历子文件夹下的所有文件与子目录,并将对应项目加入到列表与字典中
                for dirPath, dirNames, fileNames in os.walk(sub_dir_path):
                    for dirname in dirNames:
                        subdir_path = os.path.join(dirPath, dirname)
                        dir_dict['dir'][sub_dir_name]['dir'].append(subdir_path)
                    for filename in fileNames:
                        subfile_path = os.path.join(dirPath, filename)
                        subfile_md5 = self.get_md5(subfile_path)
                        if subfile_md5:
                            dir_dict['dir'][sub_dir_name]['file'][subfile_path] = subfile_md5
            elif entry.is_file():
                file_path = entry.path
                file_md5 = self.get_md5(file_path)
                if file_md5:
                    dir_dict['file'][file_path] = file_md5
        return dict(dir_dict)
    
    def get_subdir_name_list(
        self,
        return_type:str
        ):
        try:
            if return_type not in [
                'dictionary_item_added',
                'values_changed',
                'iterable_item_added',
                'iterable_item_removed']:
                raise ValueError("return_type必须是以下'dictionary_item_added','values_changed','iterable_item_added','iterable_item_removed'值中的一个")
            else:
                subdir_name_list = []
                if self.subdir_diff[return_type]:
                    for subdir_path_re in self.subdir_diff[return_type]:
                        subdir_name_re = re.search(r"root\['dir'\]\['(.*?)'\]", subdir_path_re)
                        if subdir_name_re:
                            subdir_name = subdir_name_re.group(1)
                            subdir_name_list.append(subdir_name)
                return subdir_name_list
        except ValueError:
            logging.error(f'return_type必须是以下dictionary_item_added,values_changed,iterable_item_added,iterable_item_removed值中的一个')
 
if __name__ == "__main__":
    zip = compress()
    zip.check_out(
        dir_path='/home',
        format='zip'
        )
