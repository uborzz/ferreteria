# -*- coding: utf-8 -*-

# #############################################################
#     # IMPORTS
# #############################################################

from datetime import datetime
from os import path, mkdir

from pymongo import MongoClient
from bson.objectid import ObjectId
from PIL import Image
from flask import Flask, render_template, Response, request, json, redirect, url_for, flash     # abort
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user     # login_required, UserMixin
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired     # regexp
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import _configs as cfg


# #############################################################
#     # INIT
# #############################################################

app = Flask(__name__)
app.config.from_object(cfg)     # Read config
CORS(app)                       # Config cross origin

if not path.exists(cfg.UPLOADED_PHOTOS_DEST):   # Create uploads folder if not created.
    mkdir(cfg.UPLOADED_PHOTOS_DEST)

photos = UploadSet('photos', IMAGES)    # Config for flask uploads (queremos imagenes only)
configure_uploads(app, photos)
patch_request_class(app)                # maximum file size en el request, default 16MB
# ### photos.save(filename)     # No usaremos el save, meteremos a pelo las imagenes ahi tras resize con pillow.

# #############################################################
#     # Login Manager
# #############################################################

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(username):
    u = users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])


# #############################################################
#     # Database Info
# #############################################################

db = MongoClient(cfg.DB_URI, maxPoolSize=50, wtimeout=2000)[cfg.DB_NAME]
users = db.users


#############################################################
    # Scheduler
#############################################################

# scheduler = BackgroundScheduler()
# scheduler.start()


# #############################################################
#     # Clases / forms
# #############################################################

class User:
    """ Clase user básica para usar con el LoginManager """
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class LoginForm(FlaskForm):
    """Login form to access admin page"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class OfertaForm(FlaskForm):
    """Formulario Oferta/promocion"""
    name = StringField('Nombre', validators=[DataRequired(u"Utiliza un nombre!")])
    cost = FloatField('Precio')
    desc = TextAreaField(u'Descripción', validators=[DataRequired(u"Define una descripción!")])
    image = FileField(validators=[FileAllowed(photos, u'Solo se pueden enviar imágenes!'), FileRequired(message=u'No has seleccionado un archivo!')])
    submit = SubmitField(u'Insertar')


class ModificacionOfertaForm(OfertaForm):
    image = FileField(validators=[FileAllowed(photos, u'Solo se pueden enviar imágenes!')])
    submit = SubmitField(u'Modificar')


class NotificacionForm(FlaskForm):
    """Formulario Mensaje de notificacion"""
    mensaje = TextAreaField('Modificar mensaje')
    submit = SubmitField('Modificar')


#############################################################
    # Services y DB methods
#############################################################

def get_mensaje():
    notificacion = db.notificacion.find_one()
    if notificacion:
        return notificacion['mensaje']
    else:
        return ""


def get_ofertas():
    ofertas = db.ofertas.find()
    if ofertas:
        ofertas = list(ofertas)
        for oferta in ofertas:
            oferta['cost'] = '%.2f €' % oferta['cost']  # format 2 decimals.
            oferta['image'] = photos.url(oferta['image'])
        return ofertas
    else:
        return []


def get_ofertas_admin():
    ofertas = db.ofertas.find()
    if ofertas:
        return ofertas
    else:
        return []


def no_autorizado():
    return Response(
        json.dumps({"message": "Don't hack me mon..."}),
        mimetype='application/json',
        status=401
    )

def guarda_imagen_pil(imagen):
    """
    imagen: Objeto FileStorage (de flask/werkzeug) que es de algún tipo de imagen.
    return: Nombre final fichero
    """
    filename = str(int(datetime.now().timestamp())) + "-" + secure_filename(imagen.filename)
    # filename = path.splitext(filename)[0] + ".jpg"

    pil_img = Image.open(imagen)
    pil_img.thumbnail((300, 200), Image.ANTIALIAS)
    pil_img.save(path.join(cfg.UPLOADED_PHOTOS_DEST, filename))

    return filename


#############################################################
    # Http API
#############################################################

@app.route('/')
def index():
    mensaje = get_mensaje()
    return render_template('index.html', mensaje=mensaje)


@app.route('/english')
def english():
    mensaje = get_mensaje()
    return render_template('english.html', mensaje=mensaje)


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/promociones')
def promociones():
    return render_template('promociones.html', ofertas=get_ofertas())


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        form = NotificacionForm()
        return render_template("admin.html", mensaje_notificacion=get_mensaje(), ofertas=get_ofertas_admin(), form_notificacion=form)
    else:
        flash("Se necesita login para acceder al panel de administrador.", category='info')
        return redirect(url_for("login"))


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


@app.route("/mensaje/modificar", methods=["POST"])
def modificar_mensaje():
    if current_user.is_authenticated:
        form = NotificacionForm()
        if form.validate_on_submit():
            db.notificacion.update_one({}, {"$set": {"mensaje": form.mensaje.data}}, upsert=True)
            flash("Notificación modificada correctamente", "success")
        else:
            flash("Error producido al modificar", "error")
        return redirect(url_for("admin"))
    else:
        return no_autorizado()


@app.route("/ofertas/insertar", methods=['GET', 'POST'])
def insertar_oferta():
    if current_user.is_authenticated:
        form = OfertaForm()
        if request.method == "POST" and form.validate_on_submit():

            image = form.image.data         # obtiene imagen del form y altera nombre en linea siguiente
            # filename = photos.save(image)   # guarda imagen a disco
            filename = guarda_imagen_pil(image)

            nueva_oferta = {
                'name': form.name.data,
                'desc': form.desc.data,
                'cost': form.cost.data,
                'image': filename
            }

            db.ofertas.insert_one(nueva_oferta)
            flash('Nueva oferta insertada correctamente.', 'success')
            return redirect(url_for("admin"))
        return render_template("insertar_oferta.html", title="Insertar Oferta", form=form)
    else:
        return no_autorizado()


@app.route("/ofertas/<id>", methods=['GET', 'POST'])
def modificar_oferta(id):
    if current_user.is_authenticated:
        form = ModificacionOfertaForm()

        if request.method == "POST" and form.validate_on_submit():
            nueva_oferta = {
                'name': form.name.data,
                'desc': form.desc.data,
                'cost': form.cost.data,
            }

            if form.image.data:
                image = form.image.data  # obtiene imagen del form
                # print(type(image), image.filename)
                # filename = photos.save(image)  # guarda imagen directamente a disco

                filename = guarda_imagen_pil(image)
                nueva_oferta['image'] = filename

            db.ofertas.update_one({"_id": ObjectId(id)}, {"$set": nueva_oferta}, upsert=True)
            flash('Oferta modificada correctamente.'.format(form.name.data), 'success')
            return redirect(url_for("admin"))

        elif request.method == "GET":
            oferta_seleccionada = db.ofertas.find_one({"_id": ObjectId(id)})
            foto_oferta_url = photos.url(oferta_seleccionada['image'])
            if oferta_seleccionada:
                return render_template(
                   "modificar_oferta.html",
                   title="Modificar Oferta",
                   form=form,
                   oferta_seleccionada=oferta_seleccionada,
                   foto_oferta_url=foto_oferta_url
                )
            else:
                flash('La oferta seleccionada no está ya en el sistema.', "error")
                return redirect(url_for("admin"))
        flash('Algo no ha ido bien :(', "error")
        return render_template("insertar_oferta.html", title="Insertar Oferta", form=form)
    else:
        return no_autorizado()


@app.route("/borrar_oferta/<id>", methods=['POST'])  # Equivale al "DELETE" de modificar oferta.
def borrar_oferta(id):
    if current_user.is_authenticated:
        db.ofertas.delete_one({"_id": ObjectId(id)})
        return redirect(url_for("admin"))
    else:
        return no_autorizado()


############################################################################################################
############# Tests Upload Files ###########################################################################
#############      BORRAR        ###########################################################################
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')

# @app.route("/iii", methods=["GET", "POST"])
def upload_file():
    if current_user.is_authenticated:
        form = UploadForm()
        if request.method == "POST" and form.validate_on_submit():
            form.photo.data.filename = str(int(datetime.now().timestamp())) +"-"+ secure_filename(form.photo.data.filename)
            filename = photos.save(form.photo.data)
            file_url = photos.url(filename)
        else:
            file_url = None
        return render_template('uploadimage.html', form=form, file_url=file_url)

    else:
        return no_autorizado()


########## Tests POST/GET Basicos
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

########## Tests footer

@app.route('/test')
def html_test():
    return render_template('test_footer.html')

##############################################################################################################
##############################################################################################################
##############################################################################################################


# #############################################################
#     # APP Run
# #############################################################

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run()

# if __name__ == '__main__':
#     app.run(ssl_context = 'adhoc')

