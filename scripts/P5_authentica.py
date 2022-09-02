#多参体： 有参数时，不用headers=headers_data，加files={"x":"y"}，无请求体不用加
#通过是否满足条件保留self.session作为OK和KO的全局变量session来传递是否已验证成功

import app
import json
import utils
import requests
import unittest
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

class authentica(CheckPoint):
    OK_session = None
    KO_session = None

    #前置处理
    def setUp(self):
        self.authentica_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #认证
    @parameterized.expand(build_data(filename="P5_authentica.json", params_name="keywords, realname, card_id, status_code, status, description"))
    def test001_and_003_authentica(self, keywords, realname, card_id, status_code, status, description):
        #登录
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        login_data = {
            "keywords": keywords,
            "password": app.password
        }
        response = self.authentica_api.login(self.session, headers_data, login_data)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("登录成功", response.json().get("description"))

        #认证
        authentica_data= {
            "realname": realname,
            "card_id": card_id
        }
        response = self.authentica_api.authentica(self.session, authentica_data)
        print("认证：{}".format(response.json()))
        if login_data.get("keywords") == app.authentica_phone and response.json().get("description") == "提交成功!":
            authentica.OK_session = self.session
        elif response.json().get("description") != "提交成功!":
            authentica.KO_session = self.session
        self.checkAssertEqual(status_code, response.status_code)
        self.checkAssertEqual(status, response.json().get("status"))
        self.checkAssertEqual(description, response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    #查询未认证
    def test004_query_not_authenticated(self):
        response = self.authentica_api.select_authentica(authentica.KO_session)
        print("查询未认证：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(100, response.json().get("status"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    #查询已认证
    def test005_query_certified(self):
        response = self.authentica_api.select_authentica(authentica.OK_session)
        print("查询已认证：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual("1", response.json().get("realname_card"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
