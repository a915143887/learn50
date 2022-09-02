import app
import utils
import random
import requests
import unittest
from bs4 import BeautifulSoup
from api.p2p_api import p2p_api
from checkPoint import CheckPoint

class flow_path(CheckPoint):
    session = None
    phone = "13809283612"
    imgVerifyCode = "8888"
    phone_code = "666666"
    realname = "王晓雨"
    card_id = "440682199604236311"
    amount = "10000"
    valicode = "8888"

    #前置处理
    @classmethod
    def setUpClass(cls):
        cls.flow_path_api = p2p_api()
        cls.session = requests.session()
    #后置处理
    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        sql_01 = "delete from litemall_user where id in (10031, 10032, 10033)"
        print(utils.mysql_conn.db(sql_01, app.db_database))
        sql_02 = "delete from litemall_user where id in (10034, 10035, 10036)"
        print(utils.mysql_conn.db(sql_02, app.db_database))

    def test001_register_success(self):
        #图片验证码
        r = random.random()
        response = self.flow_path_api.img_code(self.session, r)
        print("图片验证码，响应状态码：{}，响应头：{}".format(response.status_code, response.headers.get("Content-Type")))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(None, response.headers.get("Content-Type"))

        #短信验证码
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        sms_data = {
            "phone": self.phone,
            "imgVerifyCode": self.imgVerifyCode,
            "type": "reg"
        }
        response = self.flow_path_api.sms_code(self.session, headers_data, sms_data)
        print("短信验证码：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("短信发送成功", response.json().get("description"))

        #注册
        register_data = {
            "phone": self.phone,
            "password": app.password,
            "verifycode": self.imgVerifyCode,
            "phone_code": self.phone_code,
            "dy_server": "on",
            "invite_phone": ""
        }
        response = self.flow_path_api.register(self.session, headers_data, register_data)
        print("注册：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("注册成功", response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    def test002_login_success(self):
        #登录
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        login_data = {
            "keywords": self.phone,
            "password": app.password
        }
        response = self.flow_path_api.login(self.session, headers_data, login_data)
        print("登录：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("登录成功", response.json().get("description"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    def test003_authentica_success(self):
        #认证
        authentica_data = {
            "realname": self.realname,
            "card_id": self.card_id
        }
        response = self.flow_path_api.authentica(self.session, authentica_data)
        print("认证：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))
        self.checkAssertEqual("提交成功!", response.json().get("description"))

        #查看认证状态
        response = self.flow_path_api.select_authentica(self.session)
        print("查看认证状态：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual("1", response.json().get("realname_card"))
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    def test004_account_success(self):
        #开户
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self.flow_path_api.account(self.session, headers_data)
        print("开户：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))

        #第三方开户
        form_data = response.json().get("description").get("form")
        response = utils.Third_api(form_data, headers_data)
        print("第三方开户：{}".format(response.text))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual("UserRegister OK", response.text)
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()

    def test005_top_up_success(self):
        #充值验证码
        r = random.random()
        response = self.flow_path_api.top_up_code(self.session, r)
        print("充值验证码，响应状态码：{}，响应头：{}".format(response.status_code, response.headers.get("Content-Type")))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(None, response.headers.get("Content-Type"))

        #充值
        headers_data = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        top_up_data = {
            "paymentType": "chinapnrTrust",
            "amount": self.amount,
            "formStr": "reForm",
            "valicode": self.valicode
        }
        response = self.flow_path_api.top_up(self.session, headers_data, top_up_data)
        print("充值：{}".format(response.json()))
        self.checkAssertEqual(200, response.status_code)
        self.checkAssertEqual(200, response.json().get("status"))

        #第三方充值
        form_data = response.json().get("description").get("form")
        response = utils.Third_api(form_data, headers_data)
        print("第三方充值：{}".format(response.text))
        self.checkAssertEqual(200, response.status_code)
        self.assertIn("OK", response.text)
        self.checkTestResult()
    if __name__ == "__main__":
        unittest.main()
