from flask import redirect, request
from main import app
from flask_login import LoginManager
import jwt
import config


login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/get-token')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        return "success"
    except jwt.ExpiredSignatureError:
        return "ExpiredSignatureError"
    except jwt.exceptions.DecodeError:
        return "DecodeError"

if __name__ == "__main__": 
    app.run(debug=True)