import os
import shelve
import logging

class compress:
    # TODO 增加多压缩类
    SNAPSHOT_FILE = os.path.join(os.path.dirname(__file__), "snapshot")
     
    def check_out(
        self,
        dir_path:str,
        format:str
        ):
        # TODO 适配多压缩类
        """检查目标文件夹函数

        Args:
            dir_path (str): 目标文件夹
            format (str): 压缩格式
        """
        try:
            self.snapshot()
            raw_list = os.listdir(dir_path)
            if raw_list:
                self.diffsnapshot(raw_list)
                self.snapshot(raw_list)
               # if  is True:
                    #print('waiting!')
                #else:
                    #print('compressed!')
                    #self.snapshot(raw_list)

                #if os.listdir(dir_path) != snap_one:
                    #snap = os.listdir(dir_path)
                    #for dir in os.listdir(dir_path):
                        #print('compressed!')
            else:
                #snap = []
                print('waiting!')
        except FileNotFoundError:
            logging.error(f'file not find!')
            
    def snapshot(
        self,
        snap:list=[]
        ):
        """初始化快照并将快照持久化至snapshot文件中.
        
        如果快照不存在且无对应key值则进行首次初始化,若snap输入空值且文件存在且包含key值,则跳过初始化.

        Args:
            snap (list, optional): 输入要进行快照文件列表. 默认为[]以进行初始化.
        """
        if os.path.isfile(self.SNAPSHOT_FILE):
            snapshot = shelve.open(filename=self.SNAPSHOT_FILE,writeback=True)
            if snap:
                snapshot['snap'] = snap
            else:
                return True
        elif os.path.isdir(self.SNAPSHOT_FILE):
            os.removedirs(self.SNAPSHOT_FILE)
            snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
        else:
            snapshot = shelve.open(filename=self.SNAPSHOT_FILE)
        if 'snap' not in snapshot:
            snapshot['snap'] = snap
        snapshot.close()
        
    def diffsnapshot(
        self,
        diff_snapshot:list
        ):
        # TODO 返回值以对应不同的压缩类
        raw_snapshot = shelve.open(filename=self.SNAPSHOT_FILE,writeback=True)
        if set(diff_snapshot).difference(set(raw_snapshot['snap'])):
            print('compress----raw_list!!')
        elif not set(diff_snapshot).difference(set(raw_snapshot['snap'])):
            print('waiting!')
  
if __name__ == "__main__":
    zip = compress()
    zip.check_out(
        dir_path='/home/elxiaght/桌面/Mobiusite/docker/msdata/local/compress',
        format='test'
        )
    #print(os.path.dirname(__file__))
    #zip.snapshot()