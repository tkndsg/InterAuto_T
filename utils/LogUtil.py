
# 封装log工具类
# 1、创建类
import datetime
import logging
import os

from config import Conf
from config.Conf import ConfigYaml


class Logger:
    # 2、定义参数
    # 输出文件名称，loggername,日志级别
    def __init__(self, log_file, log_name, log_level, stream_log_level="debug", file_log_level="info"):
        self.log_file = log_file  # 拓展名 配置文件
        self.log_name = log_name  # log名称 参数
        self.log_level = log_level  # log总等级 配置文件
        self.stream_log_level = stream_log_level  # 控制台log等级 配置文件
        self.file_log_level = file_log_level  # 文件log等级 配置文件
    # 3、编写输出控制台或文件
        # 1、设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 2、设置log级别
        log_dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }
        self.logger.setLevel(log_dict[self.log_level])
        formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')

        if not self.logger.handlers:
            # 3、输出控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setFormatter(formatter)
            fh_stream.setLevel(log_dict[self.stream_log_level])

            # 4、输出到写入文件
            fh_file = logging.FileHandler(self.log_file)
            fh_file.setFormatter(formatter)
            fh_file.setLevel(log_dict[self.file_log_level])

            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)


# 1、初始化参数数据
# 日志文件名称，日志文件级别
# 日志文件名称 = logs目录 + 当前时间+拓展名
# logs目录
log_path = Conf.get_log_path()
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
# 拓展名
log_extension = ConfigYaml().get_conf_log_extension()
logfile = os.path.join(log_path, current_time + log_extension)
loglevel = ConfigYaml().get_conf_log_level()


# 2、对外方法，初始化log工具类，提供其他类使用
def my_log(log_name=__file__):
    return Logger(log_file=logfile, log_name=log_name, log_level=loglevel).logger


if __name__ == "__main__":
    my_log().info("this is a debug test")
