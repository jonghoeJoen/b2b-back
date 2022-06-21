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


blueprint_login = Blueprint("login", __name__, url_prefix="/login")

@blueprint_login.route("/login", methods=['POST'])
def login_get_info():
    conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
                                user = 'root',                 # 디비 접속 계정
                                password = 'root',             # 디비 접속 비번
                                db = 'temp',               # 데이터 베이스 이름
                                port = 53306,                  # 포트
                                charset = 'utf8')
    cursor = conn.cursor()
    try:
        req = request.get_json() 
        username = req['username']
        password = req['password']
        
        sql = """
            select
                password
            from tb_user
            where username=%s
        """
        # conn = pymysql.connect(host = 'meta-soft.iptime.org', # 디비 주소 //localhost
        #                         user = 'root',                 # 디비 접속 계정
        #                         password = 'root',             # 디비 접속 비번
        #                         db = 'temp',               # 데이터 베이스 이름
        #                         port = 53306,                  # 포트
        #                         charset = 'utf8')
        # cursor = conn.cursor()
        cursor.execute(sql, username)
        row = cursor.fetchone()
        if check_password_hash(row[0], password) is True:
            # JWT 토큰에는, payload와 시크릿키가 필요합니다.
            # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
            # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
            # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
            payload = {
                'id': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
            }
            token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')

            # token을 줍니다.
            # return jsonify({'result': 'success', 'token': token}), 200
            return make_response(jsonify({'result': 'success', 'token': token}), 200)
        # 찾지 못하면
        else:
            # return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
            return "300"
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        return "500"
        
    # if username is None or password is None:
    #     return redirect('/relogin')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    # user_info = User.get_user_info(user_id, user_pw)

    # if user_info['result'] != 'fail' and user_info['count'] != 0:
    #     # 사용자 객체 생성
    #     login_info = User(user_id=user_info['data'][0]['USER_ID'])
    #     # 사용자 객체를 session에 저장
    #     login_user(login_info)
    #     return redirect('/main')
    # else:
    #     return redirect('/relogin')


# 로그인 실패 시 재로그인
# @app.route('/relogin')
# def relogin():
#     login_result_text = "로그인에 실패했습니다. 다시 시도해주세요."
    
#     return render_template('common/template_login.html', login_result_text=login_result_text)


# # 로그아웃
# @app.route('/logout')
# def logout():
#     # session 정보를 삭제한다.
#     logout_user()
#     return redirect('/')