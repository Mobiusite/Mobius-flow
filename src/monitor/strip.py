import os
import shutil
import tomlkit
import logging
from appdirs import user_config_dir

class streamrip :
    """Streamrip类:用于配置streamrip
    """
    APPNAME = "streamrip"
    CONFIG_DIR = user_config_dir(APPNAME)
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")
    
    def checkout(
        self,
        download_dir: str
    ):
        """检查配置文件是否存在,若存在,则修改默认储存地址
        
        需要额外安装Streamrip

        Args:
            download_dir (str): 指定储存路径
        """
        if os.path.isfile(self.CONFIG_PATH):
            self.change_dir(
                change_download_dir=download_dir
            )
        else:
            os.makedirs(os.path.dirname(self.CONFIG_PATH), exist_ok=True)
            shutil.copy(self.DEFAULT_CONFIG_PATH,self.CONFIG_PATH)
            self.change_dir(
                change_download_dir=download_dir
            )
        logging.info(f'默认储存位置已修改为{download_dir}')
            
    def change_dir(
        self,
        change_download_dir: str
    ):
        """将默认的储存地址修改为指定``change_download_dir``

        Args:
            change_download_dir (str): 指定储存路径
        """
        with open(self.CONFIG_PATH) as r_cfg:
            streamrip_cfg = tomlkit.loads(r_cfg.read().strip())
            download_dict = streamrip_cfg['downloads']
            assert isinstance(download_dict, dict)
        if download_dict['folder'] != change_download_dir:
            download_dict['folder'] = change_download_dir
            with open(self.CONFIG_PATH,'w') as w_cfg:
                w_cfg.write(tomlkit.dumps(streamrip_cfg))
                    
if __name__  ==  '__main__':
    st =streamrip()
    st.checkout(download_dir="/home/root")