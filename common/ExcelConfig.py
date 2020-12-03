

# 定义类
class DataConfig:
    # 定义列属性  excel列名和字段对照表
    case_num = "编号"
    case_id = "用例ID"
    case_model = "模块"
    case_name = "接口名称"
    url = "请求URL"
    pre_exec = "前置条件"
    method = "请求类型"
    params_type = "请求参数类型"
    params = "请求参数"
    body = "请求体"
    expect_result = "预期结果"
    last_result = "上次结果"
    exclude_regex_paths = "diff正则排除"
    is_run = "是否运行"
    headers = "headers"
    cookies = "cookies"
    code = "status_code"
    db_verify = "数据库验证"
    note = "备注"
    host = "HOST"
