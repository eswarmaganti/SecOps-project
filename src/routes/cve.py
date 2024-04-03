import sys
import traceback
from datetime import datetime
from flask import Blueprint,request,jsonify
import traceback
import validators
import pathlib
from sqlite_db.db import CVE,db


cve = Blueprint("cve",__name__,url_prefix="/cve")


# method: GET
# access: Public
# action: Get the cve by id
@cve.get("/<string:cve_id>")
def get_cve_by_id(cve_id):
    try:
        cve_data = CVE.query.filter_by(cve_id=cve_id).first()

        if not cve_data:
            return jsonify({"error":"CVE not found"}),404

        return jsonify({"cve_id":cve_data.cve_id,"severity":cve_data.severity,"cvss":cve_data.cvss,"affected_packages":cve_data.affected_packages,"description":cve_data.description,"cwe_id":cve_data.cwe_id}),200

    except Exception as e:
        print(f"{datetime.now()} : *** Error: something went wrong while fetching cve by id - {str(e)} ***",file=sys.stderr)
        return jsonify({"message":"something went wrong, unable to fetch cve by id","status":"error"}),500



# method: GET
# access: Public
# action: Get all cve's available
@cve.get("/all")
def get_all_cves():
    try:
        cve_data = CVE.query.all()
        print(cve_data)
        if not cve_data:
            return jsonify({"error": "CVE not found"}), 404


        return jsonify([{"cve_id": item.cve_id, "severity": item.severity, "cvss": item.cvss,
                        "affected_packages": item.affected_packages, "description": item.description,
                        "cwe_id": item.cwe_id} for item in cve_data ]), 200

    except Exception as e:
        print(f"{datetime.now()} : *** Error: something went wrong while fetching cve by id - {str(e)} ***",file=sys.stderr)
        return jsonify({"message":"something went wrong, unable to fetch cve by id","status":"error"}),500


# method: POST
# access: Public
# action: Add new cve
@cve.post("/addCVE")
def add_new_cve():
    try:
        cve_id = request.json.get("cve_id","")
        severity = request.json.get("severity","")
        affected_packages = request.json.get("affected_packages","")
        cvss = request.json.get("cvss","")
        cwe_id = request.json.get("cwe_id","")
        description = request.json.get("description","")


        if not cve_id:
            return jsonify({"error":"Mandatory fields are missing, CVE ID is required"}),400
        if not severity:
            return jsonify({"error":"Mandatory fields are missing, Severity is required"}),400
        if not description:
            return jsonify({"error":"Mandatory fields are missing, Description is required"}),400

        existing_cve = CVE.query.filter_by(cve_id=cve_id).first()

        # validating for existing CWE
        if existing_cve:
            return jsonify({"error":"CVE is already present"}),400

        # creating a new record
        cve = CVE(severity=severity,cve_id=cve_id,cwe_id=cwe_id,description=description,affected_packages=affected_packages,cvss=cvss)
        db.session.add(cve)
        db.session.commit()

        return jsonify({"cve_data":{
            "cve_id":cve.cve_id,
            "severity":cve.severity,
            "affected_packages":cve.affected_packages,
            "cvss":cve.cvss,
            "cwe_id":cve.cwe_id,
            "description":cve.description
        },"message":"CVE added successfully"}),201

    except Exception as e:
        db.session.rollback()
        print(f"{datetime.now()} : *** Error: something went wrong while adding cve - {str(e)} ***",file=sys.stderr)
        return jsonify({"message":"something went wrong, unable to add cve","status":"error"}),500



# method: DELETE
# access: Public
# action: Delete a cve
@cve.delete("/<string:cve_id>")
def delete_cve_by_id(cve_id):
    try:
        cve = CVE.query.filter_by(cve_id=cve_id).first()
        if not cve:
            return jsonify({"error": "CVE not found"}), 404

        db.session.delete(cve)
        db.session.commit()
        return jsonify({"message": "CVE deleted successfully"})

    except Exception as e:
        db.session.rollback()
        print(f"{datetime.now()} : *** Error: something went wrong while fetching cve by id - {str(e)} ***",file=sys.stderr)
        return jsonify({"message":"something went wrong, unable to fetch cve by id","status":"error"}),500



# method: PUT, PATCH
# access: Public
# action: Update a cve
@cve.put("/<string:cve_id>")
@cve.patch("/<string:cve_id>")
def update_cve_by_id(cve_id):
    try:
        severity = request.json.get("severity", "")
        affected_packages = request.json.get("affected_packages", "")
        cvss = request.json.get("cvss", "")
        cwe_id = request.json.get("cwe_id", "")
        description = request.json.get("description", "")

        # fetching the existing cve
        existing_cve = CVE.query.filter_by(cve_id=cve_id).first()

        # validating for existing CWE
        if not existing_cve:
            return jsonify({"error": "CVE is not present"}), 400

        # updating a new record
        existing_cve.cve_id = cve_id
        existing_cve.severity = severity if severity else existing_cve.severity
        existing_cve.affected_packages = affected_packages if affected_packages else existing_cve.affected_packages
        existing_cve.cvss = cvss if cvss else existing_cve.cvss
        existing_cve.cwe_id = cwe_id if cwe_id else existing_cve.cwe_id
        existing_cve.description = description if description else existing_cve.description

        db.session.commit()

        return jsonify({"cve_data": {
            "cve_id": existing_cve.cve_id,
            "severity": existing_cve.severity,
            "affected_packages": existing_cve.affected_packages,
            "cvss": existing_cve.cvss,
            "cwe_id": existing_cve.cwe_id,
            "description": existing_cve.description
        }, "message": "CVE updated successfully"}), 201

    except Exception as e:
        traceback.print_exc()
        print(f"{datetime.now()} : *** Error: something went wrong while updating cve - {str(e)} ***",file=sys.stderr)
        return jsonify({"message":"something went wrong, unable to update cve","status":"error"}),500


