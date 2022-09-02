#导包
import pymysql

class mysql_conn():
    __conn = None
    __cursor = None

    #建立连接
    @classmethod
    def __get_conn(cls):
        if cls.__conn is None:
            cls.__conn = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user="root",
                                         password="root",
                                         database="tpshop2.0",
                                         charset="utf8")
        return cls.__conn

    #获取游标
    @classmethod
    def __get_cursor(cls):
        if cls.__cursor is None:
            cls.__cursor = cls.__get_conn().cursor()
        return cls.__cursor

    #编写SQL语句
    @classmethod
    def my(cls, sql):
        try:
            cursor = cls.__get_cursor()
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
