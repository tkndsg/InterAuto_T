#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import base64
import json
import sys
import xlwt


class Json2excel:
    def __init__(self):
        self.json_path = None

    def json_to_dict(self):
        try:
            self.json_path = sys.argv[1]
        except IndexError:
            self.json_path = "./example_har.har"
        # if not self.json_path.endswith(".har"):
        #     "请传文件后缀为.har的文件，谢谢"
        #     exit(0)
        with open(file=self.json_path, mode="r", encoding="utf8") as fp:
            json_data = json.load(fp)
            return json_data

    def dict_to_list(self):
        """
        host
        请求URL
        请求类型
        请求参数
        请求体
        :return:
        """
        case_dict = self.json_to_dict()
        case_list = list()
        entries = case_dict['log']['entries']
        # print(len(entries))
        for x in range(0, len(entries)):
            # 请求
            r_request_body, r_request_data, r_param = None, None, None
            r_url = case_dict['log']['entries'][x]['request']['headers'][2]['value']
            r_host = case_dict['log']['entries'][x]['request']['headers'][3]['value']
            r_have_userid = case_dict['log']['entries'][x]['request']['headers'][4]['name']
            r_method = case_dict['log']['entries'][x]['request']['method']
            if len(case_dict['log']['entries'][x]['request']['queryString']) == 0:
                r_param = None
            else:
                r_param = {}
                r_param_list = case_dict['log']['entries'][x]['request']['queryString']
                for r_param_dict in r_param_list:
                    r_param[r_param_dict["name"]] = r_param_dict["value"]

            if r_method == "POST":
                r_request_data = case_dict['log']['entries'][x]['request']['postData']
                if r_request_data['mimeType'] == "application/json":
                    r_request_body = r_request_data['text']
            if r_param is not None:
                r_url = str(r_url).split("?")[0]

            if r_have_userid == "userid" and \
                    (r_host == "explorer-beta.tratao.com" or r_url == "xremit-beta.xcurrency.com/"):
                r_headers = "LOGGED_HEADER"
            elif r_host == "explorer-beta.tratao.com" or r_url == "xremit-beta.xcurrency.com/":
                r_headers = "UNLOGGED_HEADER"
            else:
                r_headers = ""

            # 响应
            r_response_code = case_dict['log']['entries'][x]['response']['status']
            r_response_body_encoded = case_dict['log']['entries'][x]['response']['content']['text']
            r_response_body = base64.b64decode(r_response_body_encoded).decode('utf-8')
            r_host = "https://"+r_host
            if r_param is not None:
                r_param = json.dumps(r_param)
            temp_tuple = (r_host, r_url, r_method.lower(), r_param, r_request_body, r_response_code, r_headers, r_response_body)
            # print(temp_tuple)
            case_list.append(temp_tuple)
        return case_list

    def param_to_excel(self):
        case_list = self.dict_to_list()

        book = xlwt.Workbook()
        sheet = book.add_sheet(u"case")
        for case_no in range(0, len(case_list)):
            sheet.write(case_no, 4, case_list[case_no][0])  # host
            sheet.write(case_no, 5, case_list[case_no][1])  # url_path
            sheet.write(case_no, 7, case_list[case_no][2])  # request_method
            if case_list[case_no][3] is not None:
                param = str(case_list[case_no][3])
            else:
                param = None
            sheet.write(case_no, 9, param)  # param
            if case_list[case_no][4] is not None:
                request_body = str(case_list[case_no][4])
            else:
                request_body = None
            sheet.write(case_no, 10, request_body)  # request_body
            sheet.write(case_no, 13, "y")  # is_run
            sheet.write(case_no, 14, case_list[case_no][5])  # status_code
            sheet.write(case_no, 15, case_list[case_no][6])  # headers
            # sheet.write(case_no, 16, str(case_list[case_no][7]).split("\'")[1])  # response_body
            sheet.write(case_no, 16, str(case_list[case_no][7]).replace("\"", "\'"))  # response_body

        file_name = self.json_path.split("/")[-1].split(".")[-2]
        file_name = file_name+".xls"
        book.save(file_name)


if __name__ == '__main__':
    # Json2excel().json_to_dict()
    # Json2excel().dict_to_list()
    Json2excel().param_to_excel()
