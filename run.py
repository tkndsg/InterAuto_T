import os
import time

import pytest
from common import Base
from config import Conf


if __name__ == '__main__':
    report_path = Conf.get_report_path()+os.sep+"result"
    report_html_path = Conf.get_report_path()+os.sep+"html"
    pytest.main(["-s", "--alluredir", report_path, "--clean-alluredir"])
    Base.allure_report(report_path, report_html_path)
    Base.send_slack(Base.is_result_pass())
    # content = "报告已生成在：" + report_html_path + "或请前往： http://123.207.107.xx:xx/job/AutoTest_JOB 查看"
    # Base.send_mail(title="接口测试结果新鲜出炉", content=content) # 报告用jenkins的发就好
