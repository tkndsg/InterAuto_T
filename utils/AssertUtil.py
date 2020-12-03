# -*- encoding: utf-8 -*-

# 1、定义封装类
import json

from common import Base
from utils.LogUtil import my_log
from deepdiff import DeepDiff
from pprint import pprint


class AssertUtil:
    # 2、初始化数据，日志
    def __init__(self):
        self.log = my_log("AssertUtil")

    # 3、code相等

    def assert_code(self, code, expected_code):
        """
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error,code is %s,expected_code is %s" % (code, expected_code))
            raise

    # 4、body相等
    def assert_body_equal(self, body, expected_body):
        """
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("body error,body is %s,expected_body is %s" % (body, expected_body))
            raise

    # 5、body包含
    def assert_in_body(self, body, expected_body):
        """
        断言预期结果和实际结果之间的的关系是否符合预期，这里分3种情况：
        1. 以!开头的内容，表示期望「实际结果中不要包含expected」，如果包含则断言不通过
        2.1 断言内容被中括号[]包裹，其中元素以,隔开的。表示期望[]的所有元素都要包含在实际结果之中，如果有不包含的就报错([]不为空)
            2.2 如果[]前有!，也就是![开头，]结尾，则期望body中不要包含expected_body列表中的任何元素
        3. 除了上面的情况，则判断expected_body是否被包含在body中，如果没有则报错
        :param body:
        :param expected_body:
        :return:
        """
        try:
            if expected_body.startswith("![") and expected_body.endswith("]"):  # 期望多不包含
                for path_of_expect in eval(expected_body[1:]):
                    assert path_of_expect not in body
            elif expected_body.startswith("[") and expected_body.endswith("]") and expected_body != "[]":  # 期望多多包含
                for path_of_expect in eval(expected_body):
                    assert path_of_expect in body
            elif expected_body.startswith("!"):  # 期望不包含
                assert expected_body[1:] not in body  # 真正需要判断的字符不包含开头的！，故去掉
            else:  # 期望包含
                assert expected_body in body
        except Exception as e:
            self.log.error("body不符合望值!!!body is %s, expected_body is %s " % (body, expected_body))
            raise

    def assert_diff(self, expect_res, actual_res, exclude_regex_paths, ignore_order=True):
        res = DeepDiff(expect_res, actual_res, ignore_order=ignore_order, exclude_regex_paths=exclude_regex_paths)
        try:
            assert res == {}
        except:
            self.log.error("twice running result is different!{0}".format(res))
            pprint(res)
            raise

    def assert_db(self, db_verify, assert_data_exist=True):
        conn = Base.init_db("db_1")
        db_res = conn.fetchone(db_verify)
        print("数据库查询结果是{de_res}")
        self.log.debug("数据库查询结果:{}".format(str(db_res)))

        if db_res == assert_data_exist:
            pass
        else:
            if db_res:
                self.log.error("assert_db 验证失败了，期望不存在的数据存在")
            else:
                self.log.error("assert_db 验证失败了，期望存在的数据不存在")
        raise



if __name__ == '__main__':
    AssertUtil().assert_diff(123123, "123123")
