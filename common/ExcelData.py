

# 1、使用Excel工具类，获取结果list
from common import ExcelConfig
from common.Base import log
from config import Conf
from utils.ExcelUtil import ExcelUtil


class Data:
    def __init__(self, testcase_file, sheet_name):
        self.reader = ExcelUtil(testcase_file, sheet_name)

# 2、列是否运行内容，y
    def get_run_data(self):
        run_list = list()
        for line in self.reader.data():
            if str(line[ExcelConfig.DataConfig().is_run]).lower() == "y":
                # 3、保存要执行结果，放到新的列表
                run_list.append(line)
        return run_list

# 查出所有用例,并返回
    def get_case_list(self):
        run_list = list()
        for line in self.reader.data(need="all"):
            run_list.append(line)
        return run_list

# 根据用例id查出pre_exec的用例信息，并返回
    def get_case_pre(self, pre):
        run_list = self.get_case_list()
        for line in run_list:
            if pre == line["用例ID"]:
                return line
        return None


if __name__ == '__main__':
    data = Data(testcase_file="xxx/testdata.xlsx",sheet_name="业务1")
    line = data.get_case_pre("payment_01")
    print(line)




