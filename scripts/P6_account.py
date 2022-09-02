import app
import json
import utils
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

class account(CheckPoint):
    #前置处理
    def setUp(self):
        self.account_api = p2p_api()
        self.session = requests.session()
    #后置处理
    def tearDown(self):
        self.session.close()

    #开户
    @parameterized.expand(build_data(filename="P6_account.json", params_name="keywords, account_status_code, account_status, third_status_code, third_text"))
    def test001_account(self, keywords, account_status_code, account_status, third_status_code, third_text):
        #登录
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        login_data = {
            "keywords": keywords,
            "password": app.password
        }
        response = self.account_api.login(self.session, headers_data, login_data)
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("登录成功", response.json().get("description"))

        #开户
        response = self.account_api.account(self.session, headers_data)
        print("开户：{}".format(response.json()))
        self.checkAssertEqual(account_status_code, response.status_code)
        self.checkAssertEqual(account_status, response.json().get("status"))

        #第三方开户
        form_data = response.json().get("description").get("form")
        soup = BeautifulSoup(form_data, "html.parser")
        third_url = soup.form["action"]
        third_data = {}
        for n in soup.find_all("input"):
            a = n["name"]
            third_data[a] = n["value"]
        response = requests.post(url=third_url, headers=headers_data, data=third_data)
        print("第三方开户：{}".format(response.text))
        self.checkAssertEqual(third_status_code, response.status_code)
        self.assertIn(third_text, response.text)
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
