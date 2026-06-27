from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, JobApplication
from datetime import datetime
routes_blueprint = Blueprint("routes", __name__)

@routes_blueprint.route("/jobs", methods=["GET"])
@login_required
def get_jobs():

    jobs = JobApplication.query.filter_by(user_id=current_user.id).all()
    return jsonify([job.to_dict() for job in jobs]), 200

@routes_blueprint.route("/jobs", methods=["POST"])
@login_required
def create_job():
    data = request.get_json()

    if not data or not data.get("company") or not data.get("role") or not data.get("status") or not data.get("date_applied"):
        return jsonify({"error": "Company, role, status, and date applied are required."}), 400
    
    date_applied = datetime.strptime(data["date_applied"], "%Y-%m-%d").date()

    job = JobApplication(
        company=data["company"],
        role=data["role"],
        status=data["status"],
        date_applied=date_applied,
        user_id=current_user.id,
        link=data.get("link"),
        notes=data.get("notes")
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

@routes_blueprint.route("/jobs/<int:id>", methods=["PUT"])
@login_required
def update_job(id):
    data = request.get_json()
    
    if not data or not data.get("company") or not data.get("role") or not data.get("status") or not data.get("date_applied"):
        return jsonify({"error": "Company, role, status, and date applied are required."}), 400

    job = db.session.get(JobApplication, id)
    
    if not job or job.user_id != current_user.id:
        return jsonify({"error": "Job not found."}), 404
    
    date_applied = datetime.strptime(data["date_applied"], "%Y-%m-%d").date()
    
    job.company = data["company"]
    job.role = data["role"]
    job.status = data["status"]
    job.date_applied = date_applied
    job.link = data.get("link")
    job.notes = data.get("notes")
    db.session.commit()
    return jsonify(job.to_dict()), 200

@routes_blueprint.route("/jobs/<int:id>", methods=["DELETE"])
@login_required
def delete_job(id):
    job = db.session.get(JobApplication, id)

    if not job or job.user_id != current_user.id:
        return jsonify({"error": "Job not found."}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted."}), 200