from cgi import print_arguments
import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash

blueprint_favor = Blueprint("favor", __name__, url_prefix="/favor")


@blueprint_favor.route("/get-all", methods=['POST'])
def read():
    conn = None
    cursor = None
    try:
        getData = request.get_json()
        sql = "select * from tb_favorite favor JOIN tb_store store ON favor.store_id = store.id where 1=1 "
        if (getData['search']['userId']): 
            sql += "AND user_id = '" + getData['search']['userId'] + "'"
            print(sql)
        # data = (user['username'], hashed_password, user['storeName'], None, "T", now, now)
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        conn.commit()
        # return 'true' 
        return make_response(jsonify({'result': 'success', 'data': row}), 200)
    except Exception as e:
        print(e)
        return 'fail' 
    finally:
        cursor.close() 
        conn.close()


@blueprint_favor.route("/create", methods=['POST'])
def loadStoreFavor():
    conn = None
    row = None
    cursor = None
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    getData = request.get_json()
    print(getData)
    print(getData['userId'])
    try:
        data = request.get_json()
        sql = "INSERT INTO tb_favorite (user_id, store_id) VALUES (%s, %s)"
        data = (getData['userId'], getData['storeId'])
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return 'sucess'
    except Exception as e:
        print(e)
        return 'fail'
    finally:
        cursor.close() 
        conn.close()

@blueprint_favor.route("/delete", methods=['POST'])
def deltStoreFavor():
    conn = None
    row = None
    cursor = None
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    getData = request.get_json()
    print(getData)
    print(getData['userId'])
    try:
        sql = "DELETE from tb_favorite where 1=1 "
        if (getData['userId']):
            sql += "AND user_id = '" + getData['userId'] + "' "
        if (getData['storeId']):
            sql += "AND store_id = '" + getData['storeId'] + "' "
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8',
                                cursorclass = pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return 'sucess'
    except Exception as e:
        print(e)
        return 'fail'
    finally:
        cursor.close() 
        conn.close()
