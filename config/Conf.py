import os

# 1、获取项目基本路径
# 获取当前项目的绝对路径
from utils.YamlUtil import YamlReader

current = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current))  # BASE_DIR = os.cwd(__file__)  应该也行
# 定义config目录路径
_config_path = BASE_DIR + os.sep + "config"
# 定义conf.yml文件的路径
_config_file = _config_path + os.sep + "conf.yml"# 定义config目录路径
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# 定义db_conf.yml文件的路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义log文件路径
_log_path = BASE_DIR + os.sep + "logs"
# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"


def get_report_path():
    """
    获取report绝对路径
    @return:
    """
    return _report_path

def get_config_path():
    return _config_path

def get_data_path():
    return _data_path


def get_db_config_path():
    return _db_config_file


def get_config_file():
    return _config_file


def get_log_path():
    return _log_path


# 2、读取配置文件的方法
# 创建类
class ConfigYaml:
    # 初始yaml读取配置文件
    def __init__(self):
        self._config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_path()).data()

    # 定义方法获取需要信息
    def get_conf_url(self):
        return self._config["BASE"]["test"]["url"]

    def get_conf_log_level(self):
        return self._config["BASE"]["log_level"]

    def get_conf_log_extension(self):
        return self._config["BASE"]["log_extension"]

    def get_excel_file(self):
        return self._config["BASE"]["test"]["case_file"]

    def get_excel_sheet(self):
        return self._config["BASE"]["test"]["case_sheet"]

    def get_db_config_info(self, db_alias):
        """
        :db_alias: 根据db_alias获取该名称下的数据库信息
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        @return:
        """
        return self._config["email"]

    def get_global_param(self, var_name):
        return self._config["GLOBAL"][var_name]

    def get_global_params(self):
        return self._config["GLOBAL"]


if __name__ == "__main__":
    x = ConfigYaml().get_global_params()
    print(x)
    # conf_read = ConfigYaml()
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_log_extension())
    # db_conf = ConfigYaml()
    # r = db_conf.get_excel_file()
    # r1= db_conf.get_excel_sheet()
    # print(r)
    # print(r1)
    # res = ConfigYaml().get_email_info()
    # print(res)
