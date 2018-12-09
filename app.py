from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import geocoder, requests, json,request

import models,forms,json_classes
import googleapiclient
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

app = Flask(__name__)

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
   """ g = geocoder.ip('me')
    print(g.latlng)
    r = r = requests.get('127.0.0.1:5000/api/v1/todos')
    print(r)
    test = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name&key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI')
    print(json.dumps(test.json()))
    print(tert)

    test2 = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Banks&circle:200@{},{}&feilds=formatted_address,name&key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI'.format(
            g.latlng[0], g.latlng[1]))
    test3 = requests.get(
        'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=1500&feilds=formatted_address,name&type=shop&keyword=clothes&key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI'.format(
            g.latlng[0], g.latlng[1]))
    test4 = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Waitrose&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,rating&locationbias=circle:1500@{},{}&key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI'.format(
            g.latlng[0], g.latlng[1]))
    res = test3.json()
    print(test3.json())
    testArr = []
    for results in res['results']:
        for info in results:
            if info == 'name':
                testArr.append(results[info])

    for shop in testArr:
        test4 = requests.get(
            'https://maps.googleapis.com/maps/api/place/findplacefromtext/'
            'json?input={}&inputtype=textquery&fields=photos,formatted_'
            'address,name,opening_hours,rating&locationbias=circle:1500@{},{}&'
            'key=AIzaSyDxNK_Fu4JuEcP6Elc1v28nZmteG64nDyI'.format(shop,
                                                                 g.latlng[0],
                                                                 g.latlng[1]))
        print(test4.json())
        if test4.json()['candidates'][0]["rating"]:
            print(test4.json()['candidates'][0]["name"] + " "
                 + test4.json()['candidates'][0][
                   "formatted_address"] + " rating: "+"{}".
                format(test4.json()['candidates'][0]["rating"]))
        else:
            print(test4.json()['candidates'][0]["name"] + " "
                  + test4.json()['candidates'][0][
                      "formatted_address"] + " rating: " + "None")
                      """
   models.initialize()

   return render_template('test.html')


@app.route('/search')
@login_required
def search():
    user = models.User.get(id=g.user.id)
    print(user.email)
    user_pref = user.get_preferences()
    search_string = user_pref.generate_search_string()
    print('before test ')
    print(user_pref.food)
    print(user_pref.student_discount)
    print(user_pref.clothing)
    print(user_pref.technology)
    print(search_string)
    results = json_classes.SearchFetcher.get_data(search_string)
    print(results)
    return render_template('index.html', results=results)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        user = models.User.get(email=form.email.data)
        models.UserPreferences.create(user=user.id)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/userpref', methods=('GET', 'POST'))
@login_required
def userPrferences():
    user = models.User.get(id=g.user.id)
    pref = user.get_preferences()
    form = forms.PreferenceForm(obj=pref)

    if form.validate_on_submit():
        print("passed form")
        form.populate_obj(obj=pref)
        pref.save()
        return redirect(url_for('index'))

    return render_template("login.html", form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run()
