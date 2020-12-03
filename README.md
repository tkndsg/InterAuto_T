# InterAuto_T  
> 参照博学谷课程[《接口自动化测试全方案设计与开发》](https://xuexi.boxuegu.com/video.html?courseId=1484)魔改而成  
> 基于`Python`+ `pytest`+ `requests`接口自动化测试框架，主流套路，简单好用

### 一、背景
- 接口测试比较简单直观，接口自动化实现性价比高，适合作为推动测试自动化第一步

### 二、框架特点
- 通过pytest，实现Excel用例管理做参数化，生成Allure报告等
- 有diff断言，响应体字段包含等多个断言方式
- 写了个.har文件转Excel小工具协助写用例
- 接入slack和邮件双重通知，及时发现问题，解决问题

### 三、框架流程
![框架流程](https://github.com/tkndsg/InterAuto_T/blob/master/file/ProcessFramework.png)

### 四、项目结构
```
.
├── venv              # 虚拟环境
├── common            # 公共方法类
├── config            # 配置相关
├── data              # 测试数据，Execl文件，用例源文件
├── logs              # log
├── report            # 报告模块
├── utils             # 工具模块
├── testcase          # 测试用例
├── file              # 文件资源
├── run.py            # 程序主入口
├── pytest.ini        # pytest配置文件
└── requirements.txt  # 依赖第三方包
```

### 五、使用方法
#### 5.1 环境准备
1. 已提前安装下载好了IDE如：Pycharm  
2. 已配置好了Python3.x环境  
3. 电脑上安装了pip  
4. allure本地的时候需要[配置环境变量](https://www.jianshu.com/p/5c634654a38b)  
 
#### 5.2 安装下载
1. [github](https://github.com/tkndsg/InterAuto_T/)上git clone到本地  
2. 在[PyCharm](https://www.jetbrains.com/pycharm/download/)中打开项目，把本地缺少的包都导一下，或者选择自己的环境（如果很慢的话可以[配置下国内镜像源](https://blog.csdn.net/qq_39248703/article/details/88537414)）  

#### 5.3 用例编写
1. 打开/data/testdata.xlsx  
2. 在Excel中打开，照着例子写用例就行，支持全局变量和连续接口间数据传递

#### 5.4 基本配置
在/config/conf.yml文件中完成基本信息的配置

#### 5.5 调试执行
- 调试：在/testcase/test_excel_case.py 找到main方法，使用pytest方式执行即可
- 正式执行：在/run.py中用pytest的方式执行main方法即可
- 上面两种方式的区别："正式执行"后会生成allure测试报告，邮件通知(需提前在config/conf.yml中配置)和slack通知

### 六、更新记录

