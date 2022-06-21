from flask import render_template, redirect
from main import app
from flask_login import login_required
from flask_bcrypt import Bcrypt

app.config['SECRET_KEY'] = '3ildkf399dlkdlskfle2'
app.config['BCRYPT_LEVEL'] = 10

@app.route("/main")
# 로그인이 필요한 기능에 선언
@login_required
def main():
    # # menu_list = Menu().get_menu_list()
    # if menu_list['result'] == 'fail':
    #     menu_list = None
    # else:
    #     menu_list = menu_list['data']
    
    # return render_template("common/layout/layout_basic.html", 
    #         menu_list=menu_list)