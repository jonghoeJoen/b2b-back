import datetime
from tracemalloc import start
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
    per_page=20
    getData = request.get_json()
    print(getData)
    start_time = getData['startTime']
    end_time = getData['endTime']
    text = getData['text']
    user_id = getData['userId']
    conn = None
    cursor = None
    try:
        page = getData['page']
        start_at = page*per_page
        sql = """ 
            select * FROM tb_order_history history LEFT JOIN tb_store store ON history.store_id = store.id where 1=1
        """
        if (start_time != '') :
            sql += "AND history.created_date >= '" + start_time + " 00:00:00'"
        if (end_time != '') :
            sql += "AND history.created_date <= '" + end_time + " 23:59:59'"
        if (text != '') :
            sql += "AND store.store_name like '%" + text + "%'"
        if (user_id != '') :
            sql += "AND history.user_id = '" + user_id + "'"
        # sql += (" limit %s, %s", (start_at, per_page))
        print(sql)
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
