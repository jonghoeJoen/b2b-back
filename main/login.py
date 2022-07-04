import datetime
from flask import Blueprint, jsonify, make_response, redirect, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
import jwt
import config


blueprint_login = Blueprint("login", __name__, url_prefix="/api/login")

@blueprint_login.route("/login", methods=['POST'])
def login_get_info():
    conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
    cursor = conn.cursor()
    req = request.get_json() 
    username = req['username']
    password = req['password']
    try:
        sql = """
            select
                tb_user.password,
                tb_role_user.role_id,
                tb_user.id,
                tb_user.store_id
            from tb_user
            JOIN
            tb_role_user
            ON
                tb_role_user.user_id = tb_user.id
            where tb_user.username=%s
        """
        cursor.execute(sql, username)
        row = cursor.fetchone()
        print(row)
        if check_password_hash(row[0], password) is True:
            payload = {
                'username': username,
                'role': row[1],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'userId': row[2],
                'storeId': row[3]
            }
            token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')
            return make_response(jsonify({'token': token}), 200)
        else:
            print("패스워드 틀림")
            # return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
            return jsonify({'message': 'User Does Not Exist', "authenticated": False}), 401
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@blueprint_login.route("/wholesaler-login", methods=['POST'])
def wholesaler_login():
    conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
    cursor = conn.cursor()
    req = request.get_json() 
    print(req)
    try:
        sql = """
            select
                tb_user.password,
                tb_role_user.role_id,
                tb_user.id,
                tb_user.store_id,
                tb_user.username
            from tb_user
            JOIN
            tb_role_user
            ON
                tb_role_user.user_id = tb_user.id
            where tb_user.store_id = %s
        """
        
        cursor.execute(sql, str(req['storeId']))
        row = cursor.fetchone()
        print(row)
        payload = {
            'username': row[4],
            'role': row[1],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'userId': row[2],
            'storeId': row[3]
        }
        token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')
        return make_response(jsonify({'token': token}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify(e))
    finally:
        cursor.close() 
        conn.close()