# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from flask import Flask, render_template, Response, request, json, redirect, url_for, flash, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
import _configs as cfg
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Login form to access admin page"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])



class User:
    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)



app = Flask(__name__)
app.config.from_object(cfg)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])


CORS(app)   # Config cross origin

update_on_launch = False

# class LoginForm(FlaskForm):
#     username = StringField('Username')
#     password = PasswordField('Password')
#     submit = SubmitField('Submit')

# #############################################################
#     # DB_INFO
# #############################################################

db = MongoClient(cfg.DB_URI, maxPoolSize=50, wtimeout=2000)[cfg.DB_NAME]
users = db.users


#############################################################
    # Scheduler routine
#############################################################

# scheduler = BackgroundScheduler()
# scheduler.start()


#############################################################
    # Services/DB methods
#############################################################

# def get_page(kwargs):
#     pass


#############################################################
    # Http API
#############################################################
# @app.route('/')
# def home():
#     return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = users.find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logeado correctamente como usuario: {}".format(user["_id"]), category='success')
            return redirect(request.args.get("next") or url_for("admin"))
        flash("Usuario/Password incorrectos.", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Usuario desconectado.", category='success')
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return render_template("admin.html")
    else:
        flash("Se necesita login para acceder al panel de administrador.", category='info')
        return redirect(url_for("login"))


@lm.user_loader
def load_user(username):
    u = users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])

# autentioco /
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/promociones')
def promociones():
    return render_template('promociones.html')


@app.route('/test')
def html_test():
    return render_template('test_footer.html')


@app.route('/gettest')
def get_test():
    return Response(
        json.dumps({
            "result": "Ok"
        }),
        mimetype='application/json'
    )


@app.route('/posttest', methods=['POST'])
def post_test():
    return Response(
        json.dumps({
            "result": "Ok",
            "echo": request.json,
            "mimetype": request.mimetype
        }),
        mimetype='application/json'
    )

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run()

# if __name__ == '__main__':
#     app.run(ssl_context = 'adhoc')

