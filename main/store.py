import datetime
from flask import Blueprint, jsonify, make_response, request
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
import model

blueprint_shop = Blueprint("shop", __name__, url_prefix="/shop")


@blueprint_shop.route("/get-all", methods=['POST'])
def read():
    per_page=20
    conn = None
    cursor = None
    getData = request.get_json()
    print("getData")
    print(getData)
    try:
        sql = """
            select * 
            from tb_store 
            JOIN tb_code code 
            ON tb_store.building_num = code.id where 1=1 
        """
        if (getData['text'] != '') :
            sql += "AND store_name like '%" + getData['text'] + "%' "
        if (getData['buildingNum'] != '') :
            sql += "AND building_num = '" + str(getData['buildingNum']) + "' "
        if (getData['page']): 
            page = getData['page'] - 1
            start_at = page*per_page
            sql += " LIMIT " + str(start_at) + ', ' + str(per_page)
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
        return 'false'
    finally:
        cursor.close() 
        conn.close()
    # return 'tset'


@blueprint_shop.route("/create-store", methods=['POST'])
def createStore():
    conn = None
    cursor = None
    store = request.get_json()
    try:    
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        sql = """ 
            insert into tb_store (store_name, store_location, phone_no, mobile_no, account_number, building_num, address1, ceo_name, manager_name, address2, postcode, created_date, last_modified_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (store['storeName'], store['storeLocation'], store['phoneNo'], store['mobileNo'], store['accountNumber'], store['buildingNum'], store['address1'], store['ceoName'], store['managerName'], store['address2'], store['postcode'], now, now)
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return 'sucess'
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()

@blueprint_shop.route("/load", methods=['POST'])
def loadStore():
    conn = None
    row = None
    cursor = None
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    try:
        data = request.get_json()
        id = data['id']
        sql = "select * from tb_store where id = '" + id + "'"
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

@blueprint_shop.route("/get-all-paging", methods=['POST'])
def getAllPaging():
    conn = None
    cursor = None
    getData = request.get_json()
    print(getData)
    try:
        getData = request.get_json()

        # query = model.PageFragment.sortStart()
        # query += " select * from tb_store"
        # query += model.PageFragment.sortEnd()
        # query += model.PageFragment.sortEnd()
        # query 
        # sql = "select * from tb_store"
        if (getData['page']): 
            page = getData['page'] - 1
            start_at = page*per_page
            sql += " LIMIT " + str(start_at) + ', ' + str(per_page)
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
        return make_response(jsonify({'result': 'success', 'data': row}), 200)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
