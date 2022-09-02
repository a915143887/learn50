#注意：open=参数,用参数化引入参数的值，通过if open == 1则执行，来控制是否调用图片验证码接口

import app
import json
import random
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

class sms_code(CheckPoint):
    #前置处理
    def setUp(self):
        self.sms_code_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #短信验证码
    @parameterized.expand(build_data(filename="P2_sms_code.json", params_name="number, phone, imgVerifyCode, type, status_code, status, description"))
    def test001_and_005_sms_code(self, number, phone, imgVerifyCode, type, status_code, status, description):
        open = number
        if open == 1:
            #图片验证码
            r = random.random()
            response = self.sms_code_api.img_code(self.session, r)
            self.checkAssertEqual(200, response.status_code)
            self.checkAssertEqual(None, response.headers.get("Content-Type"))

        #短信验证码
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        sms_data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": type
        }
        response = self.sms_code_api.sms_code(self.session, headers_data, sms_data)
        print("短信验证码：{}".format(response.json()))
        self.checkAssertEqual(status_code, response.status_code)
        self.checkAssertEqual(status, response.json().get("status"))
        self.checkAssertEqual(description, response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

