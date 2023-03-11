import os
import time
import shutil
import logging
import qbittorrentapi

class Qbittorrent:
    """
    Qb:监控Qbittorrent与QbittorrenEE的相关自动化流程
    """
    
    def __init__(self,host,username,secret):
        """
        通过webAPI连接指定客户端并检查可用性
        
        Arguments:
            ``host``: 主机地址:端口
            ``username``: 用户名
            ``secret``: 密码
        """
        self._client = qbittorrentapi.Client(
            host=host,
            username=username,
            password=secret
        )
        while True:
            try:
                self._client.auth_log_in()
                break
            except qbittorrentapi.LoginFailed :
                logging.error('登录远程客户端失败,检查地址,用户名与密码!将于10s后重试')
            except qbittorrentapi.Forbidden403Error :
                logging.error('403:连接远程服务器被拒绝,可能服务不存在?处于黑名单中?将于10s后重试')
            except qbittorrentapi.APIConnectionError : 
                logging.error('出现API连接错误,请检查qbit是否启动?将于10s后重试')
                # raise qbittorrentapi.APIConnectionError
            time.sleep(10)
    
    def copy_tag(self,category,src,dir):
        """
        检查torrent的tag是否存在``copied``,若不存在则复制源文件/文件夹至``dir``地址下
        
        Arguments:
            ``category``: 类别名称
            ``src``: 源路径
            ``dir``: 目标路径
        """
        seeding_list=self._client.torrents_info(status_filter='completed',category=category)
        for torrent in seeding_list:
            tags_origin = str(torrent.tags)
            tags = tags_origin.split(', ')
            if 'copied' in tags:
                continue
            else:
                hash = str(torrent.hash)
                path_origin = str(torrent.content_path)
                name = path_origin.split('/')[-1]
                true_src = '{0}/{1}'.format(src.rstrip('/'),name)
                if os.path.exists(true_src):
                    try:
                        if os.path.isfile(true_src):
                            shutil.copy2(src=true_src,dst=dir)
                        elif os.path.isdir(true_src):
                            true_dir = '{0}/{1}'.format(dir.rstrip('/'),name)
                            shutil.copytree(src=true_src,dst=true_dir)
                        self._client.torrents_add_tags(tags='copied',torrent_hashes=hash)
                    except:
                        logging.error(f'目标路径错误')
                else:
                    logging.error(f'源路径错误或源文件/文件夹不存在')
                
    def del_nonetag(self):
        """
        删除没有torrent关联的tag,除了``copied``.
        """
        tags_list = self._client.torrents_tags(kwargs = [])
        
        for _tag in tags_list:
            tag = str(_tag)
            if tag == 'copied':
                continue
            elif not self._client.torrents_info(tag=tag):
                self._client.torrents_delete_tags(tags=tag)


if __name__ == '__main__' :
    qbee = Qbittorrent(host='127.0.0.1:9001',username='admin',secret='admintest')
    qbee.copy_tag(category='test',src='/home/下载/test',dir="/home/桌面")
    qbee.del_nonetag()
    