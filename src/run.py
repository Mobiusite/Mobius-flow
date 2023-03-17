import logging
from config import setconf,setlog

version = '0.1.0'

def showinfo():
    global version
    logging.info(r' ___      _______          __========')
    logging.info(r'|   \    /  _____|   /|   / /========')
    logging.info(r'| |\ \  /   |___    / |  / /=========')
    logging.info(r'| | \ \/ /| ___ \  /  | / /==========')
    logging.info(r'| |  \  / | |  \ \/ /||/ /===========')
    logging.info(r'|_|   \/  |_|   \__/ |__/========2023')
    logging.info(r'=====================================')
    logging.info(f"版本:{version} 自动化工作流 For Mobiusite")
    logging.info("正在初始化.......")
    
def run():
    setlog()
    setconf()
    showinfo()

if (__name__ == '__main__'):
    run()