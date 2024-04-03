import pathlib

from flask import Flask
from flask_cors import CORS
from routes.cve import cve
from sqlite_db.db import db
proj_base_dir = pathlib.Path().resolve()
sqlite_db_url = f"sqlite:///{proj_base_dir}/src/sqlite_db/database.db"
print(sqlite_db_url)
# initializing the flask app
app = Flask(__name__,instance_relative_config=True)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=sqlite_db_url)

# initializing the sqlite db with flask application
db.app = app
db.init_app(app)
# allowing cross-origin requests
CORS(app)

# registering blue prints
app.register_blueprint(cve)