from urllib.error import HTTPError, URLError
import pymysql as my

def loginSql(uid):
    connection = None
    row = None
    try:
        # 1. 디비 오픈
        connection = my.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'easytask',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = my.cursors.DictCursor)

        # 2. 쿼리 수행
        if connection:
            print('DB 오픈')
            ########################################3333333
            # 커서 획득
            with connection.cursor() as cursor:
                print(uid)
                # sql 준비
                sql = "select * from tb_user where username = '" + uid + "';"
                print(sql)
                # 쿼리 수행
                cursor.execute(sql)
                # 결과
                row = cursor.fetchone()
                print(row)
                print('test')
                cursor.close()
            ##############################################
    except HTTPError as e: 
        print(e)
    except URLError as e:
        print(e)
    except Exception as e:
        print('->', e)
        row = None
    finally:
        if connection:
            # 3. DB 닫기
            connection.close()
            print('DB 닫기')
    return row

def loadBank():
    connection = None
    row = None
    try:
        # 1. 디비 오픈
        connection = my.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'easytask',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = my.cursors.DictCursor)

        # 2. 쿼리 수행
        if connection:
            print('DB 오픈')
            ########################################3333333
            # 커서 획득
            with connection.cursor() as cursor:
                # sql 준비
                sql = "select * from tb_bank"
                print(sql)
                # 쿼리 수행
                cursor.execute(sql)
                # 결과
                row = cursor.fetchall()
                print(row)
                cursor.close()
            ##############################################
    except HTTPError as e: 
        print(e)
    except URLError as e:
        print(e)
    except Exception as e:
        print('->', e)
        row = None
    finally:
        if connection:
            # 3. DB 닫기
            connection.close()
            print('DB 닫기')
    return row

def loadStore():
    connection = None
    row = None
    try:
        # 1. 디비 오픈
        connection = my.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',                   # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = my.cursors.DictCursor)

        # 2. 쿼리 수행
        if connection:
            print('DB 오픈')
            ########################################3333333
            # 커서 획득
            with connection.cursor() as cursor:
                # sql 준비
                sql = "select * from tb_store"
                # 쿼리 수행
                cursor.execute(sql)
                # 결과
                row = cursor.fetchall()
                cursor.close()
            ##############################################
    except HTTPError as e: 
        print(e)
    except URLError as e:
        print(e)
    except Exception as e:
        print('->', e)
        row = None
    finally:
        if connection:
            # 3. DB 닫기
            connection.close()
            print('DB 닫기')
    return row
