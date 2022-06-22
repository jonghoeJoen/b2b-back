import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager

blueprint_order = Blueprint("order", __name__, url_prefix="/order")

@blueprint_order.route("/create-order", methods=['POST'])
def createOrder():
    conn = None
    cursor = None
    getData = request.get_json()
    orderData = getData['data']
    try:    
        for order in orderData:
            now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            sql = """ 
                insert into tb_order_history (store_id, item, color, size, quantity, created_date, last_modified_date) values(%s, %s, %s, %s, %s, %s, %s)
            """
            data = (order['store_id'] , order['item'], order['color'], order['size'], order['quantity'], now, now)
            conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                    user = 'root',                 # 디비 접속 계정
                                    password = 'root',             # 디비 접속 비번
                                    db = 'temp',               # 데이터 베이스 이름
                                    port = 53306,                  # 포트
                                    charset = 'utf8')
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            # return make_response(jsonify({'result': 'success', 'data': row}), 200)
        return 'true'
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()


@blueprint_order.route("/get-all", methods=['POST'])
def Order():
    conn = None
    cursor = None
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    try:    
        sql = """ 
            select * from tb_order_history LEFT JOIN tb_store ON tb_order_history.store_id = tb_store.id
        """
        # data = (order['store_id'] , order['item'], order['color'], order['size'], order['quantity'], now, now)
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
        return 'false'
    finally:
        cursor.close() 
        conn.close()
