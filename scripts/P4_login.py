#重点：sleep(60)
#setup():每个测试case运行前运行
#teardown():每个测试case运行完后执行
#setUpClass():必须使用@classmethod 装饰器,所有case运行前只运行一次
#tearDownClass():必须使用@classmethod装饰器,所有case运行完后只运行一次

import app
import json
import requests
import unittest
from time import sleep
from api.p2p_api import p2p_api
from checkPoint import CheckPoint
from parameterized import parameterized

def build_data(filename, params_name):
    test_data = []
    file = app.base_Dir + "/data/" + filename
    with open(file, encoding="utf-8") as f:
        json_data = json.load(f)
        for case_data in json_data:
            test_params = []
            for params in params_name.split(", "):
                test_params.append(case_data.get(params))
            test_data.append(test_params)
            print("test_params= {}".format(test_params))
        return test_data

class login(CheckPoint):
    session = None

    #前置处理
    @classmethod
    def setUpClass(cls):
        cls.login_api = p2p_api()
        cls.session = requests.session()
    #后置处理
    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    #查询未登录状态：
    def test001_query_non_login_status(self):
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self.login_api.select_login(self.session, headers_data)
        print("查询未登录状态：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(250, response.json().get("status"))
        self.checkAssertEqual("您未登陆！", response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    #登录
    @parameterized.expand(build_data(filename="P4_login.json", params_name="time, keywords, password, status_code, status, description"))
    def test002_and_009_login(self, time, keywords, password, status_code, status, description):
        sleep(time)
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        login_data = {
            "keywords": keywords,
            "password": password
        }
        response = self.login_api.login(self.session, headers_data, login_data)
        print("登录：{}".format(response.json()))
        self.checkAssertEqual(status_code, response.status_code)
        self.checkAssertEqual(status, response.json().get("status"))
        self.checkAssertEqual(description, response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    #查询已登录状态
    def test010_query_logged_in_status(self):
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self.login_api.select_login(self.session, headers_data)
        print("查询已登录状态：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("OK", response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
