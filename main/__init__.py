from flask import Flask, make_response, redirect, render_template, request,jsonify,json, session, g
from . import User
from . import login
from . import order
from . import store
from . import storeFavor
import pymysql
from flask_cors import CORS, cross_origin

app = Flask(__name__)

Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(User.blueprint_user)
app.register_blueprint(login.blueprint_login)
app.register_blueprint(order.blueprint_order)
app.register_blueprint(store.blueprint_shop)
app.register_blueprint(storeFavor.blueprint_favor)