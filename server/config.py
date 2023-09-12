# Standard library imports


# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt

from models import db
# Local imports


# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


# Define metadata, instantiate db
metadata = MetaData(naming_convention={
"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
#db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)

api = Api(app)

# Instantiate REST API
db.init_app(app)


# Instantiate CORS
CORS(app)


bcrypt = Bcrypt(app)

app.secret_key = b'\x8336T\x8c\xc7oN\xf8\xbf\xd5\nOy4\xfd'