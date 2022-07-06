import datetime
from flask import Blueprint, jsonify, make_response, request, send_file
from openpyxl import Workbook
from pymysql import Connection
import pymysql
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
import model
import math
from xlsxwriter import Workbook

blueprint_excel = Blueprint("excel", __name__, url_prefix="/api/excel")


@blueprint_excel.route("/admin-order-history", methods=['POST'])
def excelAdminOrderHistory():
    getData = request.get_json()
    conn = None
    cursor = None
    try:
        sql = """ 
        select * from (
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
        if (getData['storeId'] != '') :
            sql += " AND order_history.store_id = '" + str(getData['storeId']) + "'"
        # 주문내역 리스트 (판매처)일 경우,  
        if getData['userType'] == 'wholesaleStore':
            sql += " group by order_history.pickup_date, order_history.user_id"
        else:
             sql += " group by order_history.pickup_date, order_history.store_id"
        sql += """ ) as a 
            where 1=1"""
        if (getData['text'] != '') :
            if getData['userType'] == 'wholesaleStore':
                sql += " AND a.store_name like '%" + getData['text'] + "%'"
            else: 
                sql += " AND a.store_name like '%" + getData['text'] + "%'"
            sql += " OR a.grouped_item like '%" + getData['text'] + "%'"
        sql += """ order by a.pickup_date desc, a.created_date desc"""
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
        res = cursor.fetchall()
        # print(row)

        wb = Workbook('C:\\Users\\Y\\Downloads\\workbook.xlsx')
        worksheet = wb.add_worksheet('All Data')

        row = 0
        col = 0
        # for item in res:
        #     wb.write(item)

        for r in res: 
            order = r.keys()
            print(order)
            for key in order:
                print(r[key])
                row += 1
                worksheet.write(row, col, key)
                i =1
                # for item in r[key]:
                #     worksheet.write(row, col + i, item)
                #     i += 1
        wb.close()

        return send_file('C:\\Users\\Y\\Downloads\\workbook.xlsx')


        
        # return make_response(jsonify({'result': 'success', 'data': row}), 200)
    except Exception as e:
        print(e)
        return 'false'
    finally:
        cursor.close() 
        conn.close()        

