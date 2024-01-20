import pymysql
import os
import time
db_settings = {
  "host" : "localhost",
  "port" : 3306,
  "user" : "root" ,
  "password" : "root" ,
  "db" : "data" ,
  "charset" : "utf8",
}
def insert_data(ip,count):
 time_str=time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
 sql = 'INSERT INTO task (ip,max,cur,start_time) VALUES (%s,%s,%s,%s);'
 try:
  conn=pymysql.connect(**db_settings)
  with conn.cursor() as cursor:
    cursor.execute(sql,(ip,count,0,time_str))
    #print("insert ok")
    conn.commit()
 except Exception as e:
     #print(e)
     pass
 finally:
     conn.close()

def update_data(ip_block,value):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            sql='UPDATE task SET cur=%s WHERE ip=%s;'
            cursor.execute(sql,(value,ip_block))
            conn.commit()
    finally:
        conn.close()
