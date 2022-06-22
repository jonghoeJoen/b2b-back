import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager

blueprint_user = Blueprint("User", __name__, url_prefix="/user")

@blueprint_user.route("/customer-sign-up", methods=['POST'])
def customer_sign_up():
    conn = None
    cursor = None
    try:
        user = request.get_json()
        hashed_password = generate_password_hash(user['password'])
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            insert into tb_user (username, password, name, email, status, created_date, last_modified_date) values(%s, %s, %s, %s, %s, %s, %s)
        """
        data = (user['username'], hashed_password, user['name'], None, "T", now, now)
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, data)
        print(cursor.lastrowid)

        sql = """
            insert into tb_role_user (role_id, user_id) values(%s, %s)
        """
        data = (user['roleId'], cursor.lastrowid)
        cursor = conn.cursor()
        cursor.execute(sql, data)

        conn.commit()

        return 'success'
    except Exception as err:
        print(err)
        return "error"
    finally:
        cursor.close() 
        conn.close()

@blueprint_user.route("/seller-sign-up", methods=['POST'])
def seller_sign_up():
    user = request.get_json()
    conn = None
    cursor = None
    try:
        hashed_password = generate_password_hash(user['password'])
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        sql = """
            insert into tb_store (store_name, store_location, phone_no, mobile_no, account_number, building_num, address1, ceo_name, manager_name, address2, postcode, created_date, last_modified_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (user['storeName'], user['address'], user['phoneNo'], user['mobileNo'], None, None, None, user['name'], user['managerName'], None, None, now, now)
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, data)
        store_id = cursor.lastrowid

        sql = """
            insert into tb_user (username, password, name, email, status, created_date, last_modified_date, store_id) values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (user['username'], hashed_password, user['name'], None, "T", now, now, store_id)
        cursor = conn.cursor()
        cursor.execute(sql, data)
        user_id = cursor.lastrowid

        sql = """
            insert into tb_role_user (role_id, user_id) values(%s, %s)
        """
        data = (user['roleId'], user_id)
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return 'success'
    except Exception as err:
        print(err)
        return "error"
    finally:
        cursor.close() 
        conn.close()


