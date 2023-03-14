import time
import logging
from aria2p import API,Client,ClientException

class aria2c:
    """Aira2C类:监控aria2c通知并自动化
    """
    dir = 'src/'
    def __init__(
        self,
        port: int,
        secret: str = ""
        ):
        """连接指定JSON-RPC格式的aria2远程服务器
        
        Args:
            port (int): 指定监听端口
            secret (str): 连接aria2所需的密码
        """
        while True:
            try:
                self._client = API(
                    Client(
                        port=port,
                        secret=secret
                    )
                )
                break
            except ClientException:
                logging.error(f"使用端口:{port}链接远程aria2失败,请检查密码,将于5秒后重试.")
            time.sleep(5)

    def when_dl_compelete(
        self,
        callback
        ):
        """监听文件下载完成(做种未完成)事件
        
        Args:
            callback: 回调函数
        """
        self._client.listen_to_notifications(
            threaded=True,
            timeout=3,
            on_download_complete=callback
        )
        self._client.stop_listening()
       
    def crm_file(
        self,
        api,
        gid
        ):
        """[回调函数]:将文件/文件夹移动至指定位置,并移除源文件
        
        Args:
            api: 指定远程服务器地址
            gid: 下载任务gid
        """
        try:
            file=api.get_downloads(gids=[gid])
            api.copy_files(downloads=file,to_directory=self.dir)
            if False in api.copy_files(downloads=file,to_directory=self.dir):
                for dlstaus in file:
                    if dlstaus.is_complete is not True:
                        logging.error(f"文件/文件夹:{dlstaus.name}复制失败,请检查对应任务下载状态")
            else:
                api.remove_files(downloads=file, force=False)
        except ClientException:
            logging.error(f"回调错误:远程aria2连接失败,请检查密码是否正确")

if __name__ == "__main__": 
    A2C = aria2c(6800)
    A2C.when_dl_compelete(A2C.crm_file)
