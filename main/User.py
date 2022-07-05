import datetime
from flask import Blueprint, jsonify, make_response, request
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

blueprint_user = Blueprint("User", __name__, url_prefix="/api/user")

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

@blueprint_user.route("/get-user", methods=['GET'])
def getUser(): 
    conn = None
    cursor = None
    print(request.args)
    try: 
        sql = """
            select *
            from tb_user
            where id = %s
        """
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, str(request.args.get('id')))
        row = cursor.fetchone()
        print(row)
        return make_response(jsonify({'name': row[3], 'phone_no': row[10]}), 200)
    except Exception as err:
        print(err)
        return "error"
    finally:
        cursor.close() 
        conn.close()


@blueprint_user.route("/get-retails", methods=['POST'])
def getRetails(): 
    per_page=10
    conn = None
    cursor = None
    getData = request.get_json()
    print(getData)
    try: 
        sql = """
            select
                *
            from tb_user
            left join tb_role_user tru 
            on tru.user_id = tb_user.id
            where tru.role_id = 2
        """
        if (getData['text'] != '') :
            sql += " AND tb_user.store_name like '%" + getData['text'] + "%'"
        sql +=" order by tb_user.id desc"
        data = (getData['text'])
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        cursor.execute(sql, data)
        row = cursor.fetchall()
        print(row)

        sql = """ 
            select 
                count(*) as total_rows
            from tb_user
            left join tb_role_user tru 
            on tru.user_id = tb_user.id
            where tru.role_id = 2
        """
        if (getData['text'] != '') :
            sql += " AND tb_user.store_name like '%" + getData['text'] + "%'"
        data = (getData['text'])
        sql +=" order by tb_user.id desc"
        print(sql)
        cursor.execute(sql, data)
        total_pages = cursor.fetchall()
        print('total_pages', total_pages)
        return make_response(jsonify({'result': 'success', 'data': row, 'total_rows': total_pages}), 200)
        
    except Exception as err:
        print(err)
        return "error"
    finally:
        cursor.close() 
        conn.close()


@blueprint_user.route("/get-retail-stores", methods=['POST'])
def getRetailStores():
    per_page=10
    getData = request.get_json()
    conn = None
    cursor = None
    try:
        sql = """ 
            select * from tb_user
            left join tb_role_user tru 
            on tru.user_id = tb_user.id
            where tru.role_id = 2
        """
        print(getData)
        # if (getData['userId'] != '' and getData['userId'] != None):
        #     sql += " AND history.user_id = " + str(getData['userId'])
        # if (getData['startTime'] != '') :
        #     sql += " AND history.created_date >= '" + getData['startTime'] + " 00:00:00'"
        # if (getData['endTime'] != '') :
        #     sql += " AND history.created_date <= '" +  getData['endTime'] + " 23:59:59'"
        # if (getData['text'] != '') :
        #     sql += " AND store.store_name like '%" + getData['text'] + "%'"
        # if (getData['storeId'] != '') :
        #     sql += " AND history.store_id = '" + str(getData['storeId']) + "'"
        # if (getData['page']): 
        #     page = getData['page'] - 1
        #     start_at = page*per_page
        #     sql += " LIMIT " + str(start_at) + ', ' + str(per_page)
        # 주문내역 리스트 (판매처)일 경우,  
        # if getData['useType'] is 'customer':
        # sql += " ORDER BY history."
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
        print(row)
        
        sql = """ 
            select count(*) as total_rows from tb_user
            left join tb_role_user tru 
            on tru.user_id = tb_user.id
            where tru.role_id = 2
        """
        # if (getData['userId'] != '' and getData['userId'] != None):
        #     sql += " AND history.user_id = " + str(getData['userId'])
        # if (getData['startTime'] != '') :
        #     sql += " AND history.created_date >= '" + getData['startTime'] + " 00:00:00'"
        # if (getData['endTime'] != '') :
        #     sql += " AND history.created_date <= '" +  getData['endTime'] + " 23:59:59'"
        # if (getData['text'] != '') :
        #     sql += " AND store.store_name like '%" + getData['text'] + "%'"
        # if (getData['storeId'] != '') :
        #     sql += " AND history.store_id = '" + str(getData['storeId']) + "'"
        cursor.execute(sql)
        total_pages = cursor.fetchall()[0]['total_rows']
        
        return make_response(jsonify({'result': 'success', 'data': row, 'total_rows': total_pages}), 200)
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()
