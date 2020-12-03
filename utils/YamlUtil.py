import os

import yaml


# 1、创建类
class YamlReader:
    # 2、初始化，文件是否存在
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
           self.yamlf = yamlf
        else:
            raise FileNotFoundError("yaml文件不存在")
        self._data = None

# 3、yaml读取
    def data(self):
        if not self._data:
            try:
                with open(self.yamlf, "rb") as f:
                    self._data = yaml.safe_load(f)
            except:
                with open(self.yamlf, "rb") as f:
                    self._data = list(yaml.safe_load_all(f))
        return self._data
