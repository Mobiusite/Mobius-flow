from json import load
import logging

# 读取Json文件
json_dir = 'src/conf.json'
with open(json_dir,'r') as conf_json:
    conf=load(conf_json)

# 初始化字典
config_dist = {}
# 定义配置列表中的元组.
conf_list = ('qb','qbee','alist','aria2','upload')
conf_sublist = ('movie','tvshow','other')
       
# 检查qb;qbee;aria2;alist;upload的地址是否存在且被填写.
for maintype in conf_list:
    if ( (maintype not in conf) or (not conf[maintype])):
        logging.error(maintype + '模块不存在或为空!')
        continue
    else:
        for subtype in conf_sublist:
            if((subtype not in conf[maintype]) or (not conf[maintype][subtype])):
                logging.error(maintype + '-' + subtype + '的源地址未指定!')
                continue
            else:
# 将qb;qbee;aria2;alist;upload的源文件地址映射为字典.
                config_dist[(maintype,subtype)] = conf[maintype][subtype] 
