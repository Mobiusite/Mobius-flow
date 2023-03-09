import time
import shutil
import logging
import qbittorrentapi

class Qbittorrent:
    """
    Qb:监控Qbittorrent与QbittorrenEE的相关自动化流程
    """
    dir = '/home/elxiaght/'
    
    def __init__(self,host,username,secret):
        self.client = qbittorrentapi.Client(
            host=host,
            username=username,
            password=secret
        )
        while True:
            try:
                self.client.auth_log_in()
                break
            except qbittorrentapi.LoginFailed :
                logging.error('登录远程客户端失败,检查地址,用户名与密码!')
            except qbittorrentapi.Forbidden403Error :
                logging.error('403:连接远程服务器被拒绝,可能服务不存在?处于黑名单中?')
            except qbittorrentapi.APIConnectionError : 
                logging.error('出现API连接错误,请检查qbit是否启动?')
                # raise qbittorrentapi.APIConnectionError
            time.sleep(3)
    
    def monitor_copy(self,category):
       self.client.torrents_info(status_filter='seeding',category=category)
       for torrent in self.client.torrents_info(status_filter='seeding',category=category):
        src_path=str(torrent.content_path)
        shutil.copy(src=src_path,dst=self.dir)



if __name__ == '__main__' :
    qbee_api = Qbittorrent(host='127.0.0.1:9001',username='admin',secret='admintest')
    qbee_api.monitor_copy(category='test')