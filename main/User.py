import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager

blueprint_user = Blueprint("User", __name__, url_prefix="/user")

@blueprint_user.route("/sign-up", methods=['POST'])
def sign_up():
    conn = None
    cursor = None
    try:
        user = request.get_json()
        hashed_password = generate_password_hash(user['password'])
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            insert into tb_user (username, password, name, email, status, created_date, last_modified_date) values(%s, %s, %s, %s, %s, %s, %s)
        """
        data = (user['username'], hashed_password, user['storeName'], None, "T", now, now)
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return '200'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


