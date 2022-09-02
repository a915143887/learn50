
#第三方api
import requests
from bs4 import BeautifulSoup

def Third_api(form_data, headers_data):
    soup = BeautifulSoup(form_data, "html.parser")
    #第三方url
    third_url = soup.form["action"]
    #第三方请求体参数
    third_data = {}
    for n in soup.find_all("input"):
        a = n["name"]
        third_data[a] = n["value"]
    return requests.post(url=third_url, headers=headers_data, data=third_data)


#统一读取参数化文件的方法（通用）
import app
import json

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

#初始化日志函数
import app
import time
import logging
from logging import handlers

def init_logging():
    #创建日志器
    logger = logging.getLogger()
    #设置日志等级
    logger.setLevel(logging.INFO)
    #创建控制台处理器
    ch = logging.StreamHandler()
    #创建文件处理器
    fh = logging.handlers.TimedRotatingFileHandler(app.base_Dir + "/log/p2p-{}.log".format(time.strftime("%Y%m%d-%H%M%S")),
                                                   when='h',
                                                   interval=1,
                                                   backupCount=5,
                                                   encoding="utf-8")
    #设置格式化器
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    formatter = logging.Formatter(fmt)
    #将格式化器添加到处理器
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    #将处理器添加到日志器
    logger.addHandler(ch)
    logger.addHandler(fh)

#init_logging()
#logging.info("测试")

#连接数据库
import app
import pymysql

class mysql_conn():
    __conn = None
    __cursor = None

    #建立连接
    @classmethod
    def __get_conn(cls, db_name):
        if cls.__conn is None:
            cls.__conn = pymysql.connect(host=app.db_host,
                                         port=app.db_port,
                                         user=app.db_user,
                                         password=app.db_password,
                                         database=db_name,
                                         charset="utf8")
        return cls.__conn

    #获取游标
    @classmethod
    def __get_cursor(cls, db_name):
        if cls.__cursor is None:
            cls.__cursor = cls.__get_conn(db_name).cursor()
        return cls.__cursor

    #编写sql语句
    @classmethod
    def db(cls, sql, db_name):
        try:
            cursor = cls.__get_cursor(db_name)
            cursor.execute(sql)
            if sql.split(" ")[0].lower() == "select":
                return cursor.fetchall()
            else:
                cls.__conn.commit()
                return cursor.rowcount
        except Exception as e:
            cls.__conn.rollback()
            return e
        finally:
            cls.__close_cursor()
            cls.__close_conn()

    #关闭游标
    @classmethod
    def __close_cursor(cls):
        if cls.__cursor is True:
            cls.__cursor.close()

    #关闭连接
    @classmethod
    def __close_conn(cls):
        if cls.__conn is True:
            cls.__conn.close()
