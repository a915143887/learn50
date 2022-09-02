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

class img_code(CheckPoint):
    #前置处理
    def setUp(self):
        self.img_code_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #图片验证码
    @parameterized.expand(build_data(filename="P1_img_code.json", params_name="t, status_code, headers_data"))
    def test001_and_004_img_code(self, t, status_code, headers_data):
        type = t
        if type == "int":
            self.r = random.randint(1, 10000000000)
        elif type == "float":
            self.r = random.random()
        elif type == "null":
            self.r = ""
        elif type == "letter":
            self.r = ''.join(random.sample("qwertyuioplkjhgfdsazxcvbnm", 6))

        response = self.img_code_api.img_code(self.session, self.r)
        print("图片验证码，响应状态码：{}，响应头：{}".format(response.status_code, response.headers.get("Content-Type")))
        self.checkAssertEqual(status_code, response.status_code)
        self.checkAssertEqual(headers_data, response.headers.get("Content-Type"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
