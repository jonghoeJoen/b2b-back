from flask import jsonify, make_response, redirect, request
from main import Cors, app
# import jwt
import config
import model


# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/get-token', methods=["POST","GET"])
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        return make_response(jsonify({'result': payload, 'token': token_receive}), 200)
    except jwt.ExpiredSignatureError:
        return "ExpiredSignatureError"
    except jwt.exceptions.DecodeError:
        return "DecodeError"

# @app.route('/dddd', methods=["POST","GET"])
# def dddd():
#     print("_______________________________________________________________")
#     print(model.PageFragment.limitOffset())
#     print("후" + model.PageFragment.limitOffset() % ('12', '34'))

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port = 5000)