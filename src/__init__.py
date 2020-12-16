from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from flask_login import LoginManager
from flask_migrate import Migrate 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_swap.db'
app.config['SECRET_KEY']='YourSecretKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 



app.config.from_pyfile('config.cfg')

mail = Mail(app)

urlSTS = URLSafeTimedSerializer(app.config["SECRET_KEY"])


db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

migrate=Migrate(app,db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u"Please login first!"
login_manager.session_protection = "strong"


from src.admin import routes
from src.products import routes
from src.carts import carts
from src.customers import routes
from src.emails import emails
from src.payments import payments