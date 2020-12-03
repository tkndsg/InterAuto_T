import json
import os
import re
import subprocess

from jsonpath import jsonpath

from config import Conf
from config.Conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from utils.EmailUtil import SendEmail
from utils.LogUtil import my_log
from utils.MysqlUtil import Mysql
from utils.RequestsUtil import Request
from utils.SlackUtil import SlackUtil

p_data = '\${(.*)}\$'
log = my_log("Base")
assert_util = AssertUtil()


def init_db(db_alias):
    db_info = Conf.ConfigYaml().get_db_config_info(db_alias)
    # 2、初始化数据库信息，通过配置
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])

    # 3、初始化mysql对象
    conn = Mysql(host, user, password, name, charset, port)
    # print(conn)
    return conn


def json_parse(data):
    '''
    json.loads()函数是将json格式数据转换为字典
    可以这么理解，json.loads()函数是将  字符串转化为字典
    @param data:
    @return:
    '''
    if data:
        try:
            res = json.loads(data)
        except:
            res = data
    else:
        res = data
    return res


def run_api(url, method, params=None, body=None, header=None, cookie=None):
    request = Request()
    if str(method).lower() == "get":
        res = request.get(url, params=params, headers=header, cookies=cookie)
    elif str(method).lower() == "post":
        res = request.post(url, params=params, json=body, headers=header, cookies=cookie)
    elif str(method).lower() == "put":
        res = request.put(url, json=body, params=params, headers=header, cookies=cookie)
    elif str(method).lower() == "delete":
        res = request.delete(url, params=params, headers=header, cookies=cookie)
    else:
        log.error("请求方法 method 错误：method写成了 %s" % method)
        raise
    return res


# 为有前置条件的用例把前置的结果替换成最终的参数
def get_pre_exec_correlation(headers, cookies, params, body, urls, pre_res):
    # 找到这5个参数中的哪些字段需要被替换
    headers_para, cookies_para, params_para, body_para, urls_para \
        = find_fields_need_replace(headers, cookies, params, body, urls)

    # 待替换列表若有值，在pre_res中的取到对应字段值，填回原接口参数中
    if len(headers_para) != 0:
        for i in range(len(headers_para)):
            headers_field_data = jsonpath(pre_res, f"$..{headers_para[i]}")[0]
            headers = res_sub(headers, headers_field_data, pattern_data=headers_para[i])
    if len(cookies_para) != 0:
        for i in range(len(cookies_para)):
            cookies_data = jsonpath(pre_res, f"$..{cookies_para[i]}")[0]
            cookies = res_sub(cookies, cookies_data, pattern_data=cookies_para[i])
    if len(params_para) != 0:
        for i in range(len(params_para)):
            params_data = jsonpath(pre_res, f"$..{params_para[i]}")[0]
            params = res_sub(params, params_data, pattern_data=params_para[i])
    if len(body_para) != 0:
        for i in range(len(body_para)):
            body_data = jsonpath(pre_res, f"$..{body_para[i]}")[0]
            body = res_sub(body, body_data, pattern_data=body_para[i])
    if len(urls_para) != 0:
        for i in range(len(urls_para)):
            urls_data = jsonpath(pre_res, f"$..{urls_para[i]}")[0]
            urls = res_sub(urls, urls_data, pattern_data=urls_para[i])
    return headers, cookies, params, body, urls


def res_find(data, pattern_data=p_data):
    """
    查找
    @param data:默认为\${(.*)}\$
    @param pattern_data:
    @return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)  # 找下预设了几个字段需要通过关联来获取，结果是个列表
    # print(f"re_res{re_res}")
    return re_res


def res_sub(data, replace, pattern_data=p_data):
    """
    替换
    @param data:
    @param replace:
    @param pattern_data:
    @return:
    """
    if pattern_data != p_data:
        pattern_data = p_data.replace("(.*)", pattern_data)
        print(f"被替换的正则变更为pattern_data{pattern_data}")
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        instead_res = re.sub(pattern, replace, data)
        return instead_res
    return data


def find_fields_need_replace(headers, cookies, params, body, url):
    """
    验证请求中是否有${}$需要结果关联的
    1.如果有，就取出${}$关联中的数据，
    2.如果没有关联，就不做处理，返回原来的数据
    """
    fields_need_replace_on_headers = ""
    fields_need_replace_on_cookies = ""
    fields_need_replace_on_params = ""
    fields_need_replace_on_body = ""
    fields_need_replace_on_url = ""
    if "${" in headers:
        fields_need_replace_on_headers = res_find(headers)
        print("\n从前置用例中的headers取")
    if "${" in cookies:
        fields_need_replace_on_cookies = res_find(cookies)
        print("\n从前置用例中的cookies取")
    if "${" in params:
        fields_need_replace_on_params = res_find(params)
        print("\n从前置用例中的params取")
    if "${" in body:
        fields_need_replace_on_body = res_find(body)
        print("\n从前置用例中的body取")
    if "${" in url:
        fields_need_replace_on_url = res_find(url)
        print("\n从前置用例中的urls取")
    return fields_need_replace_on_headers, fields_need_replace_on_cookies, fields_need_replace_on_params, fields_need_replace_on_body, fields_need_replace_on_url


def allure_report(report_path, report_html):
    """
    生成allure报告
    @param report_path:
    @param report_html:
    @return:
    """
    report_env_conf = Conf.get_report_path() + os.sep + "environment.properties"
    # 执行命令 allure generate
    # allure_cmd =
    # subprocess 执行命令
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    log.info("报告地址：%s" % report_path)
    copy_allure_environment_cmd = "cp %s %s" % (report_env_conf, report_path)
    res = subprocess.call(allure_cmd, shell=True)
    res_env = subprocess.call(copy_allure_environment_cmd, shell=True)
    try:
        if res == 0:
            log.info("allure报告生成成功！")
    except:
        log.error("执行用例失败，请检查一下测试环境配置")
        raise


def send_mail(report_html_path="", content="", title="测试"):
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(
        smtp_addr=smtp_addr,
        username=username,
        password=password,
        recv=recv,
        title=title,
        content=content,
        file=report_html_path
    )
    email.send_mail()
    log.info("邮件发送已执行")


def send_slack(s_type):
    """
    根据传入的期望，发送slack消息
    @param s_type:  希望发送测试通过的消息或测试不通过的消息，True为通过。
    @return:
    """
    slackutil = SlackUtil()
    if s_type is True:
        slackutil.sendpass()
        log.info("用例执行通过，Slack消息发送成功")
    elif s_type is False:
        slackutil.sendfail()
        log.info("用例执行不通过，Slack消息发送成功")
    elif s_type == "result":
        slackutil.sendresult()
        log.info("Slack消息发送成功，仅链接")
    else:
        log.error("测试统计出的结果有问题，没有发slack")


def is_result_pass():
    file_name = Conf.get_report_path() + os.sep + "html/widgets/summary.json"
    with open(file_name, encoding='UTF-8') as f:
        data = json.load(f)
        fail_num = data["statistic"]["failed"]
        if fail_num == 0:
            log.info("接口测试通过")
            return True
        else:
            log.error("接口有报错")
            return False


if __name__ == '__main__':
    is_result_pass()
