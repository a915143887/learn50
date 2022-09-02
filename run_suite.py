#导包
import time
import unittest
from tools.HTMLTestRunner import HTMLTestRunner
from scripts.P1_img_code import img_code
from scripts.P2_sms_code import sms_code
from scripts.P3_register import register
from scripts.P4_login import login
from scripts.P5_authentica import authentica
from scripts.P6_account import account
from scripts.P7_top_up_code import top_up_code
from scripts.P8_top_up import top_up

#封装测试套件
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(img_code))
suite.addTest(unittest.makeSuite(sms_code))
suite.addTest(unittest.makeSuite(register))
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(authentica))
suite.addTest(unittest.makeSuite(account))
suite.addTest(unittest.makeSuite(top_up_code))
suite.addTest(unittest.makeSuite(top_up))

#指定报告存放位置
#report = "./report/report-{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
report = "./report/report.html"

#打开文件流
with open(report, "wb") as e:
    #创建运行器
    runner = HTMLTestRunner(e, title="p2p测试报告")
    #运行
    runner.run(suite)

