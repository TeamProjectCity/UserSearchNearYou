from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import geocoder,requests
import googleapiclient




app = Flask(__name__)

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
FLASK_DEBUG=1
@app.route('/')
def hello_world():
    g = geocoder.ip('me')
    print(g.city)
    """r = r = requests.get('127.0.0.1:5000/api/v1/todos')
    print(r)"""
    test = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI')


    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=80)

