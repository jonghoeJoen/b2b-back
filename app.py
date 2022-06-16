from multiprocessing import connection
from flask import Flask, redirect, request,jsonify,json
from flask_cors import CORS, cross_origin
from database.d1 import *


app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/dataentry", methods=["POST","GET"])
def submitData():
    response_object = {'status':'success'}
    if request.method == "POST":
        post_data = request.get_json()
        
        name = post_data.get('name')
        department  = post_data.get('department')

        print(name)
        print(department)        
        print()

        uid = name
        data = loginSql(uid)
        
        response_object['message'] ='Data added!'
        response_object['data'] = data
        return jsonify(response_object)

@app.route("/dash", methods=["POST","GET"])
def loadData():
    response_object = {'status':'success'}
    if request.method == "POST":
        post_data = request.get_json()
        
        name = post_data.get('name')
        
        data = loadBank()
        
        response_object['message'] ='Data added!'
        response_object['data'] = data
        return jsonify(response_object)

@app.route('/test')
def daum():
    return redirect("http://localhost:8080/")

@app.errorhandler(404)
def page_not_found(error):
    return "페이지가 없습니다. URL를 확인 하세요", 404

if __name__ == '__main__':
    app.run(debug=True)