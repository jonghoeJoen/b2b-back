import datetime
from flask import Blueprint, jsonify, make_response, request
import pymysql

blueprint_order = Blueprint("order", __name__, url_prefix="/order")

@blueprint_order.route("/create-order", methods=['POST'])
def createOrder():
    conn = None
    cursor = None
    getData = request.get_json()
    orderData = getData['data']
    print(orderData)
    try:    
        for order in orderData:
            now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            sql = """ 
                insert into tb_order_history (store_id, user_id, item, color, size, quantity, created_date, last_modified_date, pickup_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (order['store_id'], order['user_id'], order['item'], order['color'], order['size'], order['quantity'], now, now, order['pickupDate'])
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
    conn = None
    cursor = None
    try:
        sql = """ 
            select *,
            user.name as user_name,
            user.mobile_no as user_mobile_no
            FROM tb_order_history history 
            LEFT JOIN tb_store store 
            ON history.store_id = store.id
            LEFT JOIN tb_user user 
            ON history.user_id = user.id where 1=1
        """
        print(getData)
        if (getData['userId'] != '' and getData['userId'] != None):
            sql += " AND history.user_id = " + str(getData['userId'])
        if (getData['startTime'] != '') :
            sql += " AND history.created_date >= '" + getData['startTime'] + " 00:00:00'"
        if (getData['endTime'] != '') :
            sql += " AND history.created_date <= '" +  getData['endTime'] + " 23:59:59'"
        if (getData['text'] != '') :
            sql += " AND store.store_name like '%" + getData['text'] + "%'"
        if (getData['storeId'] != '') :
            sql += " AND history.store_id = '" + str(getData['storeId']) + "'"
        if (getData['page']): 
            page = getData['page'] - 1
            start_at = page*per_page
            sql += " LIMIT " + str(start_at) + ', ' + str(per_page)
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
            select count(*) as total_rows
            FROM tb_order_history history 
            LEFT JOIN tb_store store 
            ON history.store_id = store.id
            LEFT JOIN tb_user user 
            ON history.user_id = user.id where 1=1
        """
        if (getData['userId'] != '' and getData['userId'] != None):
            sql += " AND history.user_id = " + str(getData['userId'])
        if (getData['startTime'] != '') :
            sql += " AND history.created_date >= '" + getData['startTime'] + " 00:00:00'"
        if (getData['endTime'] != '') :
            sql += " AND history.created_date <= '" +  getData['endTime'] + " 23:59:59'"
        if (getData['text'] != '') :
            sql += " AND store.store_name like '%" + getData['text'] + "%'"
        if (getData['storeId'] != '') :
            sql += " AND history.store_id = '" + str(getData['storeId']) + "'"
        cursor.execute(sql)
        total_pages = cursor.fetchall()[0]['total_rows']
        
        return make_response(jsonify({'result': 'success', 'data': row, 'total_rows': total_pages}), 200)
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()


@blueprint_order.route("/save-order-list", methods=['POST'])
def modifyOrderList():
    conn = None
    cursor = None
    getData = request.get_json()
    try:    
        for order in getData:
            print("datadtatatadtataewrawdfdfaesdf")
            print(order['available_status'])
            now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            sql = """
                insert into tb_order_history (id, store_id, user_id, item, color, size, quantity, available_status, comment, created_date, last_modified_date) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE `available_status` = VALUES(`available_status`), `comment` = VALUES(`comment`), `last_modified_date` = VALUES(`last_modified_date`)
                """
            data = (order['id'], order['store_id'], order['user_id'], order['item'], order['color'], order['size'], order['quantity'], order['available_status'], order['comment'], order['created_date'], now)
            conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                    user = 'root',                 # 디비 접속 계정
                                    password = 'root',             # 디비 접속 비번
                                    db = 'temp',               # 데이터 베이스 이름
                                    port = 53306,                  # 포트
                                    charset = 'utf8')
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        return 'true'
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()

@blueprint_order.route("/get-all-date", methods=['POST'])
def OrderByDate():
    per_page=20
    getData = request.get_json()
    conn = None
    cursor = None
    try:
        sql = """ 
            select 
                group_concat(order_history.id separator '~#~') as grouped_id,
                group_concat(order_history.item separator '~#~') as grouped_item,
                group_concat(order_history.color separator '~#~') as grouped_color,
                group_concat(order_history.size separator '~#~') as grouped_size,
                group_concat(order_history.quantity separator '~#~') as grouped_quantity,
                group_concat(order_history.available_status separator '~#~') as grouped_status,
                group_concat(order_history.comment separator '~#~') as grouped_comment,
                user.name as user_name,
                user.store_name as user_store_name,
                tb_store.store_name as store_name,
                user.mobile_no as user_mobile_no,
                order_history.pickup_date,
                order_history.user_id,
                order_history.store_id,
                DATE_FORMAT(order_history.created_date, '%Y-%m-%d %H:%i:%s') as created_date
            FROM tb_order_history order_history 
            LEFT JOIN tb_store
            ON order_history.store_id = tb_store.id
            LEFT JOIN tb_user user 
            ON order_history.user_id = user.id where 1=1
        """
        print(getData)
        if (getData['userId'] != '' and getData['userId'] != None):
            sql += " AND order_history.user_id = " + str(getData['userId'])
        if (getData['startTime'] != '') :
            sql += " AND order_history.pickup_date >= '" + getData['startTime'] + "'"
        if (getData['endTime'] != '') :
            sql += " AND order_history.pickup_date <= '" +  getData['endTime'] + "'"
        if (getData['text'] != '') :
            if getData['userType'] == 'wholesaleStore':
                sql += " AND user.store_name like '%" + getData['text'] + "%'"
            else: 
                sql += " OR tb_store.store_name like '%" + getData['text'] + "%'"
            sql += " OR order_history.item like '%" + getData['text'] + "%'"
        if (getData['storeId'] != '') :
            sql += " AND order_history.store_id = '" + str(getData['storeId']) + "'"
        # 주문내역 리스트 (판매처)일 경우,  
        if getData['userType'] == 'wholesaleStore':
            sql += " group by order_history.pickup_date, order_history.user_id"
        else:
             sql += " group by order_history.pickup_date, order_history.store_id"
        sql += " order by order_history.pickup_date desc, created_date desc"
        if (getData['page']): 
            page = getData['page'] - 1
            start_at = page*per_page
            sql += " LIMIT " + str(start_at) + ', ' + str(per_page)
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
            select 
                count(*) as total_rows
            FROM tb_order_history order_history 
            LEFT JOIN tb_store store 
            ON order_history.store_id = store.id
            LEFT JOIN tb_user user 
            ON order_history.user_id = user.id where 1=1
        """
        if (getData['userId'] != '' and getData['userId'] != None):
            sql += " AND order_history.user_id = " + str(getData['userId'])
        if (getData['startTime'] != '') :
            sql += " AND order_history.created_date >= '" + getData['startTime'] + " 00:00:00'"
        if (getData['endTime'] != '') :
            sql += " AND order_history.created_date <= '" +  getData['endTime'] + " 23:59:59'"
        if (getData['text'] != '') :
            sql += " AND store.store_name like '%" + getData['text'] + "%'"
        if (getData['storeId'] != '') :
            sql += " AND order_history.store_id = '" + str(getData['storeId']) + "'"
        cursor.execute(sql)
        total_pages = cursor.fetchall()[0]['total_rows']
        
        return make_response(jsonify({'result': 'success', 'data': row, 'total_rows': total_pages}), 200)
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()        


@blueprint_order.route("/update-order-list", methods=['POST'])
def updateOrderList():
    conn = None
    cursor = None
    getData = request.get_json()
    try:    
        conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
        cursor = conn.cursor()
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        insert_data = []
        for order in getData:
            data = (order['item'], order['color'], order['size'], order['quantity'], order['available_status'], order['comment'], now, str(order['id']))
            insert_data.append(data)
        
        print(insert_data)

        sql = """
            update tb_order_history set item = %s, color = %s, size = %s, quantity = %s, available_status = %s, comment = %s, last_modified_date = %s 
            where id = %s
            """
        
        cursor.executemany(sql, insert_data)
        conn.commit()
        return 'true'
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()