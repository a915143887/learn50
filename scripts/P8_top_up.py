import app
import json
import random
import requests
import unittest
from bs4 import BeautifulSoup
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

class top_up(CheckPoint):
    #前置处理
    def setUp(self):
        self.top_up_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #充值
    @parameterized.expand(build_data(filename="test018_top_up.json", params_name="keywords, paymentType, amount, formStr, valicode, top_up_status_code, top_up_status, description"))
    def test001_top_up(self, keywords, paymentType, amount, formStr, valicode, top_up_status_code, top_up_status, description):
        #登录
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        json_data = {
            "keywords": keywords,
            "password": app.password
        }
        response = self.top_up_api.login(self.session, headers_data, json_data)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("登录成功", response.json().get("description"))

        #充值验证码
        r = random.random()
        response = self.top_up_api.top_up_code(self.session, r)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(None, response.headers.get("Content-Type"))

        #充值
        top_up_data = {
            "paymentType": paymentType,
            "amount": amount,
            "formStr": formStr,
            "valicode": valicode
        }
        response = self.top_up_api.top_up(self.session, headers_data, top_up_data)
        print("充值：{}".format(response.json()))
        self.checkAssertEqual(top_up_status_code, response.status_code)
        self.checkAssertEqual(top_up_status, response.json().get("status"))
        for i in response.json().get("description"):
            if u'\u4e00' <= i <= u'\u9fff':
                self.checkAssertEqual(description, response.json().get("description"))
                break
            else:
                form_data = response.json().get("description").get("form")
                soup = BeautifulSoup(form_data, "html.parser")
                third_url = soup.form["action"]
                #第三方url：print(third_url)
                third_data = {}
                for n in soup.find_all("input"):
                    a = n["name"]
                    third_data[a] = n["value"]
                #第三方参数：print(third_data)
                response = requests.post(url=third_url, headers=headers_data, data=third_data)
                print("第三方充值：{}".format(response.text))
                self.checkAssertEqual(200, response.status_code)
                self.checkAssertEqual("NetSave OK", response.text)
                break
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
