import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
import model

blueprint_code = Blueprint("code", __name__, url_prefix="/api/code")


@blueprint_code.route("/get-all", methods=['POST'])
def loadCode():
    conn = None
    cursor = None
    getData = request.get_json()
    print(getData)
    try:
        getData = request.get_json()
        sql = "select * from tb_code where 1=1 "
        if (getData['parent_id'] != '') :
            sql += "AND parent_id = '" + getData['parent_id'] + "' "
            print(sql)
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
        return make_response(jsonify({'result': 'success', 'data': row}), 200)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()