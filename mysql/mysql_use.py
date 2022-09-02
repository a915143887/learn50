from mysql.mysql_conn import mysql_conn
sql = "select * from tp_goods where goods_id = 46"
a = mysql_conn.my(sql)
print(a)
