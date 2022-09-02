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

class register(CheckPoint):
    #前置处理
    def setUp(self):
        self.register_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #注册
    @parameterized.expand(build_data(filename="P3_register.json", params_name="phone, imgVerifyCode, password, verifycode, phone_code, dy_server, invite_phone, status_code, status, description"))
    def test_001_and_008_register(self, phone, imgVerifyCode, password, verifycode, phone_code, dy_server, invite_phone, status_code, status, description):
        #图片验证码
        r = random.random()
        response = self.register_api.img_code(self.session, r)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(None, response.headers.get("Content-Type"))

        #短信验证码
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        sms_data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": "reg"
        }
        response = self.register_api.sms_code(self.session, headers_data, sms_data)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("短信发送成功", response.json().get("description"))

        #注册
        register_data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": dy_server,
            "invite_phone": invite_phone
        }
        response = self.register_api.register(self.session, headers_data, register_data)
        print("注册：{}".format(response.json()))
        self.checkAssertEqual(status_code, response.status_code)
        self.checkAssertEqual(status, response.json().get("status"))
        self.checkAssertEqual(description, response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
