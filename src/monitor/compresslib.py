import os
import re
import shelve
import logging
import hashlib
from deepdiff import DeepDiff

class compress:
    # TODO 增加多类压缩
    def check_out(
        self,
        dir_path:str,
        format:str
    ):
        # TODO 适配多类压缩
        # TODO 适配解压操作
        """初始化并检查目标文件夹是否发生变化,并根据压缩格式进行压缩/解压

        Args:
            dir_path (str): 目标文件夹
            format (str): 压缩格式
        """
        self.raw_dir_path = dir_path
        try:
            if format not in ['rar','zip','7z','tar','targz','E_targz']:
                raise ValueError("format必须是以下'rar','zip','7z','tar','targz','E_targz'值中的一个")
            else:
                self.SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), format)
                self.SNAPSHOT_FILE = os.path.join(self.SNAPSHOT_PATH, "snapshot")
                self.snapshot()
            raw_dict = self.get_dirdict(dir_path)
            if raw_dict:
                if self.diffsnapshot(raw_dict):
                    dif_list = self.diffsnapshot(raw_dict)
                    for item in dif_list:
                        if format in ['zip','7z','tar','E_targz']:
                            if re.search(r'\.zip\.$', item):
                                self.subdir_name
                            if re.search(r'\.7z$', item):
                                self.subdir_name
                            if re.search(r'\.tar$', item):
                                self.subdir_name
                        if format == 'targz':
                            if re.search(r'\.tar\.gz$', item):
                                self.subdir_name
                else:
                    logging.info('快照对比无变化,等待下一次checkout')
                self.snapshot(raw_dict)
        except FileNotFoundError:
            logging.error(f'file not find!')
        except ValueError:
            logging.error(f'format必须是以下rar,zip,7z,tar,targz,E_targz值中的一个')
            
    def snapshot(
        self,
        snapshot:dict={}
    ):
        """初始化快照并将字典快照持久化至snapshot文件中.
        
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
        """对比原快照字典和现行文件目录所扫描的字典,如果原快照字典为空则直接返回现行字典,否则进行对比.

        Args:
            diff_snapshot (dict): 现行文件目录所扫描的字典

        Returns:
            list: 一个列表,其中包含文件路径和子目录路径
        """
        raw_snapshot = shelve.open(filename=self.SNAPSHOT_FILE,writeback=True)
        file_diff_list = []
        subdir_diff_list = []
        if raw_snapshot['snapshot']:
            self.file_diff = DeepDiff(
                raw_snapshot['snapshot'],
                diff_snapshot,
                exclude_paths="root['dir']"
            ).to_dict()
            self.subdir_diff = DeepDiff(
                raw_snapshot['snapshot'], 
                diff_snapshot,
                exclude_paths="root['file']"
            ).to_dict()
            raw_snapshot.close()
            if self.file_diff:
                origin_file_path_list = []
                for type in ['dictionary_item_added','values_changed']:
                    origin_file_path_list.extend(self.get_file_path_list(type))
                file_diff_list = list(set(origin_file_path_list))
            if self.subdir_diff:
                origin_subdir_path_list = []
                for type in ['dictionary_item_added','values_changed','iterable_item_added','iterable_item_removed']:
                    origin_subdir_path_list.extend(self.get_subdir_path_list(type))
                subdir_diff_list = list(set(origin_subdir_path_list))
        else:
            file_diff_list = list(diff_snapshot['file'])
            for self.subdir_name in list(diff_snapshot['dir']):
                subdir_path = os.path.join(self.raw_dir_path,self.subdir_name)
                subdir_diff_list.append(subdir_path)
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
        """遍历文件目录并序列化为字典

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
    
    def get_subdir_path_list(
        self,
        return_type:str
    ) -> list:
        """返回一个包含发生变化的子目录路径的列表

        Args:
            return_type (str): 目标类型

        Raises:
            ValueError: 输入的目标类型不符合标准

        Returns:
            list: 返回一个列表,包含发生变化的子目录路径.若无,则返回一个空列表.
        """
        subdir_path_list = []
        try:
            if return_type not in [
                'dictionary_item_added',
                'values_changed',
                'iterable_item_added',
                'iterable_item_removed'
            ]:
                raise ValueError("return_type必须是以下'dictionary_item_added','values_changed','iterable_item_added','iterable_item_removed'值中的一个")
            else:
                if return_type in self.subdir_diff:
                    for subdir_path_re in self.subdir_diff[return_type]:
                        subdir_name_re = re.search(r"root\['dir'\]\['(.*?)'\]", subdir_path_re)
                        if subdir_name_re:
                            self.subdir_name = subdir_name_re.group(1)
                            subdir_path = os.path.join(self.raw_dir_path,self.subdir_name)
                            subdir_path_list.append(subdir_path)
        except ValueError:
            logging.error(f'return_type必须是以下dictionary_item_added,values_changed,iterable_item_added,iterable_item_removed值中的一个')
        return subdir_path_list
    
    def get_file_path_list(
        self,
        return_type:str
    ) -> list:
        """返回一个包含发生变化的文件路径的列表

        Args:
            return_type (str): 目标类型

        Raises:
            ValueError: 输入的目标类型不符合标准

        Returns:
            list: 返回一个列表,包含发生变化的文件路径.若无,则返回一个空列表.
        """
        file_path_list = []
        try:
            if return_type not in [
                'dictionary_item_added',
                'values_changed'
            ]:
                raise ValueError("return_type必须是以下'dictionary_item_added','values_changed'值中的一个")
            else:
                if return_type in self.file_diff:
                    for file_path_re in self.file_diff[return_type]:
                        file_path_group = re.search(r"root\['file'\]\['(.*?)'\]", file_path_re)
                        if file_path_group:
                            file_path = file_path_group.group(1)
                            file_path_list.append(file_path)
        except ValueError:
            logging.error(f'return_type必须是以下dictionary_item_added,values_changed值中的一个')
        return file_path_list
 
if __name__ == "__main__":
    zip = compress()
    zip.check_out(
        dir_path='/home',
        format='zip'
        )
