from urllib.error import HTTPError, URLError
import pymysql

# pdialect+driver://username:password@host:port/database
# engine = sqlalchemy.create_engine('mariadb+mariadbconnector://root:root@meta-soft.iptime.org:53306/temp')

SQL_CONNECTION = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')