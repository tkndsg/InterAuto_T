import os


# 目的： 参数化，pyetest list
import xlrd
from xlutils import copy

from config import Conf


# 1、验证文件是否存在，存在读取，不存在报错
class ExcelUtil:
    def __init__(self, excel_file, sheet_by):
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.sheet_by = sheet_by
        else:
            raise FileNotFoundError("Excel文件不存在")
        self._data = list()

    def write_back(self, row, col, content):
        # workbook = xlrd.open_workbook(self.excel_file, formatting_info=True)
        workbook = xlrd.open_workbook(self.excel_file, formatting_info=True)
        copy_wb = copy.copy(workbook)
        new_sheet = copy_wb.get_sheet(self.sheet_by)
        new_sheet.write(row, col, content)
        copy_wb.save(self.excel_file)
        print("写入成功")

    def get_row_num_by_case_num(self, case_num):
        workbook = xlrd.open_workbook(self.excel_file, formatting_info=True)
        from_sheet = workbook.sheet_by_name(self.sheet_by)
        all_case_num = from_sheet.col_values(0, 0, None)
        num = all_case_num.index(case_num)
        return num

    # 2、读取sheet方法，名称，索引
    def data(self, need=None):
        if not self._data or need == "all":  # 需要找pre的时候和第一次进来的时候要重新读
            work = xlrd.open_workbook(self.excel_file)
            if len(self.sheet_by) != 0:  # sheet_by中存的是配置好的，sheet[模块，用例]模式的数据
                # print("执行以下项目+模块{}".format(self.sheet_by))
                sheet_names = self.sheet_by.keys()  # 取出所有配置中的要执行的表名
                # print("执行以下项目{}".format(sheet_names))

                for sheet_name in sheet_names:  # 对每个表逐一处理，取出「所有指定 模块或用例名 的」用例放在一起
                    sheet = work.sheet_by_name(sheet_name)  # 去到某张表
                    # 3、读取sheet内容
                    # 返回list，元素：字典
                    # 格式[{"a":"a1","b":"b1"},{"a":"a2","b":"b2"}]
                    # 1.获取首行的信息(标题)
                    title = sheet.row_values(0)
                    # 2.遍历测试行，与首行组成dict,放在list里
                    # 2.1 循环，过滤首行，从1开始
                    # 2.2 与首行组成字典，放在list里
                    for row in range(1, sheet.nrows):
                        model_or_caseid = self.sheet_by[sheet_name]  # 列出需要这个表中的哪些模块或者用例
                        if not model_or_caseid:  # 如果这个value为None直接break无需筛选了
                            break
                        col_values = sheet.row_values(row)
                        if "all" in model_or_caseid or "ALL" in model_or_caseid or need == "all":
                            self._data.append(dict(zip(title, col_values)))
                        elif col_values[1] in model_or_caseid or col_values[2] in model_or_caseid:
                            self._data.append(dict(zip(title, col_values)))
                    # print(self._data)
            else:
                NoSheetException = Exception("项目一个都不执行 异常")
                raise NoSheetException
        return self._data


# 4、结果返回
if __name__ == "__main__":
    sheet = ExcelUtil("xx/testdata.xlsx", 0)
    sheet.data()