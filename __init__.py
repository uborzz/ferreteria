# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from flask import Flask, render_template, Response, request, json, redirect, url_for, flash, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
import _configs as cfg
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, regexp
from wtforms.validators import Length


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


class OfertaForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    cost = FloatField('Precio')
    desc = TextAreaField('Descripción')
    image = FileField('Imagen') #, validators=[regexp('^[^/]\.jpg$')])
    submit = SubmitField('Enviar')


class NotificacionForm(FlaskForm):
    mensaje = TextAreaField('Modificar mensaje')
    submit = SubmitField('Modificar')


app = Flask(__name__)
app.config.from_object(cfg)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


# @lm.user_loader
# def load_user(username):
#     u = app.config['USERS_COLLECTION'].find_one({"_id": username})
#     if not u:
#         return None
#     return User(u['_id'])


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

def get_mensaje():
    notificacion = db.notificacion.find_one()
    if notificacion:
        return notificacion['mensaje']
    else:
        return ""


def get_ofertas():
    ofertas = db.ofertas.find()
    if ofertas:
        return ofertas
    else:
        return []


#############################################################
    # Http API
#############################################################
# @app.route('/')
# def home():
#     return render_template('home.html')


@app.route("/mensaje/modificar", methods=["POST"])
def modificar_mensaje():
    form = NotificacionForm()
    if form.validate_on_submit():
        db.notificacion.update_one({}, {"$set": {"mensaje": form.mensaje.data}}, upsert=True)
        flash("notificacion modificada correctamente", "success")
    else:
        flash("error producido al modificar", "error")
    return redirect(url_for("admin"))


@app.route("/ofertas/insertar", methods=['GET', 'POST'])
def insertar_oferta():
    form = OfertaForm()
    if request.method == "POST" and form.validate_on_submit():
        print(form.data)
        nueva_oferta = {
            'name': form.data['name'],
            'cost': form.data['cost'],
            'desc': form.data['desc'],
            'image': form.data['image']
        }
        res = db.ofertas.insert_one(nueva_oferta)
        print(res)
        flash('Nueva oferta insertada correctamente. Nombre de la oferta: {}'.format(form.name.data), 'success')
        return redirect(url_for("admin"))
    return render_template("insertar_oferta.html", title="Insertar Oferta", form=form)


@app.route("/ofertas/<id>", methods=['GET', 'POST', 'DELETE'])
def modificar_oferta(id):
    form = OfertaForm()
    if request.method == "POST" and form.validate_on_submit():
        print(form.data)
        nueva_oferta = {
            'name': form.data['name'],
            'cost': form.data['cost'],
            'desc': form.data['desc'],
            'image': form.data['image']
        }
        db.ofertas.update_one({"_id": ObjectId(id)}, {"$set": nueva_oferta}, upsert=True)
        flash('Oferta con el nombre: {} modificada correctamente.'.format(form.name.data), 'success')
        return redirect(url_for("admin"))
    elif request.method == "GET":
        oferta_seleccionada = db.ofertas.find_one({"_id": ObjectId(id)})
        if oferta_seleccionada:
            return render_template("modificar_oferta.html", title="Modificar Oferta", form=form, oferta_seleccionada=oferta_seleccionada)
        else:
            flash('La oferta seleccionada no está ya en el sistema.', "error")
            return redirect(url_for("admin"))


@app.route("/borrar_oferta/<id>", methods=['GET', 'POST', 'DELETE'])
def borrar_oferta(id):
    db.ofertas.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("admin"))


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
        form = NotificacionForm()
        return render_template("admin.html", mensaje_notificacion=get_mensaje(), ofertas=get_ofertas(), form_notificacion=form)
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
    mensaje = get_mensaje()
    return render_template('index.html', mensaje=mensaje)


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/promociones')
def promociones():
    return render_template('promociones.html', ofertas=get_ofertas())


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

