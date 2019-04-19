# -*- coding: utf-8 -*-
import json
import requests
from datetime import datetime
from flask import Flask, render_template, Response, request, jsonify
import _configs as cfg
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
update_on_launch = False


# #############################################################
#     # DB_INFO
# #############################################################

# client = MongoClient(cfg.mongo_uri, maxPoolSize=50, wtimeout=2000)
# db = client['ddbb']  # database
# collection = db['main_collection']  # collection


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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/productos')
def productos():
    return render_template('productos.html')


@app.route('/promociones')
def promociones():
    return render_template('promociones.html')


@app.route('/localizacion')
def localizacion():
    return render_template('localizacion.html')


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
        json_util.dumps({
            "result": "Ok",
            "echo": request.json,
            "mimetype": request.mimetype
        }),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

# if __name__ == '__main__':
#     app.run(ssl_context = 'adhoc')

