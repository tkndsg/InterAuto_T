import requests


# 1、创建封装get方法
from utils.LogUtil import my_log


# def requests_get(url, headers=None):
# # 2、发送requests get 请求
#     r = requests.get(url,headers=headers)
# # 3、活动结果响应内容
#     code = r.status_code
#     try:
#         body = r.json()
#     except:
#         body = r.text()
# # 4、内容存到字典
#     res = dict()
#     res["code"]=code
#     res["body"]=body
# # 5、字典返回
#     return res
#
#
# 1、创建封装post方法
def requests_post(url, headers=None, json=None):
    # 2、发送requests post 请求
    r = requests.post(url, headers=headers, json=json)
    # 3、活动结果响应内容
    code = r.status_code
    try:
        body = r.json()
    except:
        body = r.text()
    # 4、内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body
# 5、字典返回
    return res


# 重构
# 1、构建类
class Request:
    # 2、定义公共方法
    def __init__(self):
        self.log = my_log("Request")
    # 1.增加方法的参数，根据参数来验证方法是get还是post，用以请求

    def requests_api(self, url, data=None, headers=None, json=None, cookies=None, method="get", params=None, **kwargs):
        # 拼接请求逻辑
        proxies = {'http': 'http://localhost:8998', 'https': 'http://localhost:8998'}
        if method == "post":
            # r = requests.post(url, data=data, headers=headers, params=params, json=json, cookies=cookies,
            # proxies=proxies, verify=False)  # 用作抓包调试用
            r = requests.post(url, data=data, headers=headers, params=params, json=json, cookies=cookies)
            # self.log.info("这是一条POST请求")
        elif method == "get":
            r = requests.get(url, data=data, params=params, headers=headers, json=json, cookies=cookies)
            # r = requests.get(url, data=data, headers=headers, params=params, json=json, cookies=cookies,
            #                  proxies=proxies, verify=False)
            # self.log.info("这是一条GET请求")
        elif method == "put":
            r = requests.put(url, data=data, params=params, headers=headers, json=json, cookies=cookies)
            # r = requests.put(url, data=data, headers=headers, params=params, json=json, cookies=cookies,
            #                   proxies=proxies, verify=False)
            # self.log.info("这是一条PUT请求")
        elif method == "delete":
            r = requests.delete(url, data=data, params=params, headers=headers, json=json, cookies=cookies)
            # self.log.info("这是一条delete请求")

    # 2.重复的内容，复制进来
        # 公用的响应处理逻辑
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 4、内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 5、字典返回
        return res

# 3、重构get/post/put/delete方法
    def get(self, url, **kwargs):
        return self.requests_api(url, method="get", **kwargs)

    def post(self, url, **kwargs):
        return self.requests_api(url, method="post", **kwargs)

    def put(self, url, **kwargs):
        return self.requests_api(url, method="put", **kwargs)

    def delete(self, url, **kwargs):
        return self.requests_api(url, method="delete", **kwargs)
