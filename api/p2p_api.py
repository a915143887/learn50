import app

class p2p_api():
    def __init__(self):
        #获取图片验证码url
        self.img_code_url = app.base_Url + "/common/public/verifycode1/{}"
        #获取短信验证码url
        self.sms_code_url = app.base_Url + "/member/public/sendSms"
        #注册url
        self.register_url = app.base_Url + "/member/public/reg"
        #登录url
        self.login_url  = app.base_Url + "/member/public/login"
        #查询登录状态url
        self.select_login_url = app.base_Url + "/member/public/islogin"
        #认证url
        self.authentica_url = app.base_Url + "/member/realname/approverealname"
        #查询认证url
        self.select_authentica_url = app.base_Url + "/member/member/getapprove"
        #开户url
        self.account_url = app.base_Url + "/trust/trust/register"
        #充值验证码url
        self.top_up_code_url = app.base_Url + "/common/public/verifycode/{}"
        #充值url
        self.top_up_url = app.base_Url + "/trust/trust/recharge"

    #图片验证码
    def img_code(self, session, r):
        self.img_code_url = self.img_code_url.format(r)
        return session.get(url=self.img_code_url)

    #短信验证码
    def sms_code(self, session, headers_data, sms_data):
        return session.post(url=self.sms_code_url, headers=headers_data, data=sms_data)

    #注册
    def register(self, session, headers_data, register_data):
        return session.post(url=self.register_url, headers=headers_data, data=register_data)

    #登录
    def login(self, session, headers_data, login_data):
        return session.post(url=self.login_url, headers=headers_data, data=login_data)

    #查看登录状态
    def select_login(self, session, headers_data):
        return session.post(url=self.select_login_url, headers=headers_data)

    #认证（多参体）
    def authentica(self, session, authentica_data):
        return session.post(url=self.authentica_url, data=authentica_data, files={"x":"y"})

    #查询认证
    def select_authentica(self, session):
        return session.post(url=self.select_authentica_url)

    #开户
    def account(self, session, headers_data):
        return session.post(url=self.account_url, headers=headers_data)

    #充值验证码
    def top_up_code(self, session, r):
        self.top_up_code_url = self.top_up_code_url.format(r)
        return session.get(url=self.top_up_code_url)

    #充值
    def top_up(self, session, headers_data, top_up_data):
        return session.post(url=self.top_up_url, headers=headers_data, data=top_up_data)
