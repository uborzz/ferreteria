## Web informativa tienda

Web app hecha en 3 ratos para mostrar info de la ferretería del viejo.

### Hecha con...

Flask y Mongo. Se ha metido una pequeña sección de publicar ofertas por trastear un poco algunas funciones de flask:
flask_wtf, wtforms, flask_uploads y flask_login, así como el almacenado de imagenes.

### fichero _config.py

Tiene la info no pública, es de la siguiente forma:

```
WTF_CSRF_ENABLED = True
SECRET_KEY = 'h3r3isd4k3y'
DB_URI = "mongodb://127.0.0.1:27017"
DB_NAME = 'tienda_db'
UPLOADED_PHOTOS_DEST = "./uploads"

DEBUG = True
```

### Corriendo en:
* [Ferretería Marcial](http://ferreteriamarcial.uborzz.es)