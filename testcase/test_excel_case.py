import json
import os
import allure
import pytest
import common.Constant as Const
from common import ExcelConfig, Base, ExcelData
from config import Conf
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log

# 获取待执行用例的数据列表
case_file = os.path.join(Conf.get_data_path(), Conf.ConfigYaml().get_excel_file())
sheet_name = Conf.ConfigYaml().get_excel_sheet()
Data_init = ExcelData.Data(case_file, sheet_name)
run_list = Data_init.get_run_data()

# log初始化并开始记录执行内容
log = my_log(__file__.split("/")[-1])
sheet_name_keys = str(list(sheet_name.keys()))
log.info(
    "\n\n\n\n=====测试用例Excel文件:%s====="
    "\n=====执行sheet_name:%s====="
    "\n=====sheet表中共%s条用例需执行=====\n"
    % (case_file, sheet_name_keys, str(len(run_list))) + "=" * 96
)
setattr(Const.GetConst, "EXEC_MODULAR", sheet_name_keys)

# 获取预设好的参数，便于全局使用
data_key = ExcelConfig.DataConfig
global_params = Conf.ConfigYaml().get_global_params()


class TestExcel:
    @pytest.mark.parametrize("case", run_list)
    def test_run(self, case):
        # excel中取得用例数据
        case_num = case[data_key.case_num]
        host = case[data_key.host]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        note = case[data_key.note]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        body = case[data_key.body]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        last_result = case[data_key.last_result]
        exclude_regex_paths = case[data_key.exclude_regex_paths]
        db_verify = case[data_key.db_verify]

        # 如果是预设的常用参数就替换下
        if headers in global_params.keys():
            headers = global_params[headers]
        if host in global_params.keys():
            host = global_params[host]
        url = host + case[data_key.url]

        # 如果有参数中有需要执行前置用例的，就执行前置用例并替换参数
        if pre_exec:
            pre_case = Data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies, params, body, url \
                = Base.get_pre_exec_correlation(headers, cookies, params, body, url, pre_res)

        headers = Base.json_parse(headers)
        cookies = Base.json_parse(cookies)
        params = Base.json_parse(params)
        body = Base.json_parse(body)

        # 上面把数据都准备完成了，真正发请求
        res = Base.run_api(url, method, params, body, headers, cookies)

        # allure报告信息
        allure.dynamic.feature(sheet_name_keys)
        allure.dynamic.story(case_model)
        allure.dynamic.title(case_id + case_name)
        desc = "<font color='red'>请求URL：</font>{0}<BR/>" \
               "<font color='red'>请求方法：</font>{1}<BR/>" \
               "<font color='red'>预期结果：</font>{2}<BR/>" \
               "<font color='red'>实际结果：</font>{3}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # log记录
        log.info("=====接口【%s】的用例【%s%s】已执行！=====" % (case_name, case_id, note))
        log.debug("\n测试用例预期：%s \n测试用例执行结果：%s" % (str(expect_result), str(res)))

        # 响应状态码及响应体字符串包含断言
        assert_util = AssertUtil()
        assert_util.assert_code(res["code"], code)
        assert_util.assert_in_body(str(res["body"]), str(expect_result))

        # 响应体的diff断言
        if exclude_regex_paths != "skip_diff":
            if last_result:
                expect_result_for_diff = json.loads(json.dumps(eval(last_result)))
                if len(exclude_regex_paths) > 5:
                    exclude_regex_paths = eval(exclude_regex_paths)
                else:
                    exclude_regex_paths = None
                assert_util.assert_diff(expect_result_for_diff, res, exclude_regex_paths=exclude_regex_paths)
            else:
                from utils.ExcelUtil import ExcelUtil
                sheet_by = getattr(Const.GetConst(), (case_num[0:1]).upper())
                excel_util = ExcelUtil(excel_file=case_file, sheet_by=sheet_by)
                case_row = excel_util.get_row_num_by_case_num(case_num)
                excel_util.write_back(case_row, 16, str(res))

        # 数据库断言
        if db_verify:
            assert_util.assert_db(db_verify)

    def run_pre(self, pre_case):
        # excel中取得用例数据
        host = pre_case[data_key.host]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        body = pre_case[data_key.body]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        # 是预设常用的参数时替换下
        if headers in global_params.keys():
            headers = global_params[headers]
        if host in global_params.keys():
            host = global_params[host]
        url = host + pre_case[data_key.url]

        # 数据类型转换为dict
        headers = Base.json_parse(headers)
        cookies = Base.json_parse(cookies)
        params = Base.json_parse(params)
        body = Base.json_parse(body)

        # 前置用例请求结果返回
        res = Base.run_api(url, method, params, body, headers, cookies)
        print("前置用例执行结果：%s" % res)
        return res


if __name__ == '__main__':
    pytest.main(["-s", "test_excel_case.py"])
    # Base.allure_report(report_path,report_html_path)
    # Base.send_mail(title="接口测试报告结果",content=report_html_path)
