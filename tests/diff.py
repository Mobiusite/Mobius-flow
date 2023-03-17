# 导入deepdiff模块
import re
from deepdiff import DeepDiff

# 创建两个嵌套字典
d1 = {}
d2 = {}

# 使用DeepDiff比较两个字典的差异
#ddiff = DeepDiff(d1, d2,exclude_paths="root['dir']").to_dict()
# ddiff.custom_report_result(report_type='set_item_added',level=1)
# 最终目的是:输出dir目录下的新增的子目录和修改过的子目录.added,modified
#print(ddiff)
#for subdir_path in ddiff['values_changed']:
 #   print(subdir_path)
  #  subdir_name = re.search(r"root\['dir'\]\['(.*?)'\]", subdir_path)
   # if subdir_name:
    #    value = subdir_name.group(1)
     #   print(value)
print(list(d2['dir']))
