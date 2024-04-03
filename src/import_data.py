from sqlite_db.db import db,CVE
import pathlib
import csv

# creating all the tables
db.create_all()

# the csv file path to import data into db
import_csv_file_path = f"{pathlib.Path().resolve()}/src/data/cve_data.csv"

# reading the csv file data using csv parser
with open(import_csv_file_path,newline='') as f:
    reader = csv.reader(f)
    next(reader)
    cve_data = list(map(tuple,reader))

# inserting the data into db
try:
    for record in cve_data:
        db_record = CVE(cve_id=record[0],severity=record[1],cvss=record[2],affected_packages=record[3],description=record[4],cwe_id=record[5])
        db.session.add(db_record)
    else:
        db.session.commit()
except Exception as e:
    print(f'*** Error: Error occurred while saving the data to sqlite DB - {str(e)} ***')
    db.session.rollback()