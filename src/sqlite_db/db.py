from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime

# initializing the sqlalchemy
db = SQLAlchemy()

class CVE(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    cve_id = db.Column(db.String,unique=True, nullable=False)
    severity  = db.Column(db.String,nullable=False)
    cvss = db.Column(db.String,nullable=False)
    affected_packages = db.Column(db.String,nullable=False)
    description = db.Column(db.Text,nullable=False)
    cwe_id = db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"<CVE {self.cve_id}>"