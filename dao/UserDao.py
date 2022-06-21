import pymysql
import db_connector

SQL_CONNECTION = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')

class MyEmpDao:
    def __init__(self):
        pass

    def getUsers():
        with SQL_CONNECTION: 
            with SQL_CONNECTION.cursor() as cursor: 
                ret = []
                sql = "select * from tb_user";
                cursor.execute(sql)
                
                rows = cursor.fetchall()
                for e in rows:
                    temp = {'id':e[0],'username':e[1],'password':e[2], 'name':e[3], 'email':e[4], 'last_modified_password_date':e[5], 'status':e[6], 'created_date':e[7], 'last_modified_date':e[8] }
                    print(e)
                    ret.append(temp)
                
                db_connector.SQL_CONNECTION.commit()
                db_connector.SQL_CONNECTION.close()
                return ret
    
    # def insEmp(self, empno, name, department,phone):
    #     db = pymysql.connect(host='localhost', user='root', db='python', password='python', charset='utf8')
    #     curs = db.cursor()
        
    #     sql = '''insert into emp (empno, name, department, phone) values(%s,%s,%s,%s)'''
    #     curs.execute(sql,(empno, name, department,phone))
    #     db.commit()
    #     db.close()
    
    # def updEmp(self, empno, name, department,phone): 
    #     db = pymysql.connect(host='localhost', user='root', db='python', password='python', charset='utf8')
    #     curs = db.cursor()
        
    #     sql = "update emp set name=%s, department=%s, phone=%s where empno=%s"
    #     curs.execute(sql,(name, department, phone, empno))
    #     db.commit()
    #     db.close()
    # def delEmp(self, empno):
    #     db = pymysql.connect(host='localhost', user='root', db='python', password='python', charset='utf8')
    #     curs = db.cursor()
        
    #     sql = "delete from emp where empno=%s"
    #     curs.execute(sql,empno)
    #     db.commit()
    #     db.close()
 