import re
import logging
from json import load

# 初始化设置字典.
config_dist = {}

# 读取conf.Json文件.
with open('src/conf.json','r') as conf_json:
    conf=load(conf_json)

# 日志初始化--日志等级默认WARNGING,输出到shell.
def setlog():
    global conf
    if(('logs' not in conf) or 
       (not conf['logs'])):
        logging.basicConfig(
            format='[%(asctime)s]%(levelname)s: %(message)s', 
            datefmt='%Y/%m/%d %I:%M:%S %p', 
            level=logging.INFO)
# 若logs非空,判断log_level是否存在.
    elif('log_level' not in conf['logs']):
        try:
            raise SyntaxError
        except:
            logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', 
                                datefmt='%Y/%m/%d %I:%M:%S %p', 
                                level=logging.INFO)
            logging.error('若logs非空,则log_level必须存在')
            return None
    elif((conf['logs']['log_level']) or 
         (('log_level' and 'log_dir') in conf['logs'])):
        try:
            if (re.match('debug',conf['logs']['log_level'],re.I)):
                loglevel = logging.DEBUG
            elif (re.match('info|default',conf['logs']['log_level'],re.I)):
                loglevel = logging.INFO
            elif (re.match('warning|warn',conf['logs']['log_level'],re.I)):
                loglevel = logging.WARNING
            elif (re.match('error',conf['logs']['log_level'],re.I)):
                loglevel = logging.ERROR
            else:
                raise SyntaxError
            if ('log_dir' in conf['logs']):
                logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', 
                                    datefmt='%Y/%m/%d %I:%M:%S %p', 
                                    filename=conf['logs']['log_dir'], 
                                    encoding='utf-8', 
                                    level=loglevel)
            else:
                logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', 
                                    datefmt='%Y/%m/%d %I:%M:%S %p', 
                                    level=loglevel)   
        except:
            logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', 
                                datefmt='%Y/%m/%d %I:%M:%S %p', 
                                level=logging.INFO)
            logging.error('非法log_level或log_dir值')
            return None
    else:
        logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', 
                            datefmt='%Y/%m/%d %I:%M:%S %p', 
                            level=logging.INFO)

# 设置初始化.
def setconf():
    global config_dist
    global conf
# 定义配置列表中的元组.
    conf_list = ('qb','qbee','alist','aria2','upload')
    conf_sublist = ('movie','tvshow','other')
# 检查qb;qbee;aria2;alist;upload的地址是否存在且被填写.
    for maintype in conf_list:
        if ( (maintype not in conf['files']) or 
            (not conf['files'][maintype])):
            logging.error("{0}模块不存在或为空".format(maintype))
            continue
        else:
            for subtype in conf_sublist:
                if((subtype not in conf['files'][maintype]) or 
                   (not conf['files'][maintype][subtype])):
                    logging.error("{0}-{1}的源地址未指定!".format(maintype,subtype))
                    continue
                else:
# 将qb;qbee;aria2;alist;upload的源文件地址映射为字典.
                    config_dist[(maintype,subtype)] = conf['files'][maintype][subtype]
                    
if __name__ == '__main__':
    print('=================TEST MODE:SETLOG===================')
    setlog()
    logging.debug('当前为DEBUG')
    logging.info('当前为INFO')
    logging.warning('当前为WARNING')
    logging.error('当前为ERROR')
    print('=================TEST MODE:SETCONF===================')
    setconf()
    print(config_dist)