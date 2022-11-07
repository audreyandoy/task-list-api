from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.routes_helper import *
from app.models.task import Task 
from datetime import date 

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as err:
        error_message(f"Invalid data", 400)
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201


@task_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = Task.query

    sort = request.args.get("sort")
    if sort == "desc":
        task_query = task_query.order_by(Task.title.desc())
    elif sort == "asc":
        task_query = task_query.order_by(Task.title.asc())

    tasks = task_query.all()
    task_response = [task.to_dict() for task in tasks]
    return jsonify(task_response), 200


@task_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = get_record_by_id(Task, id)
    return {
        "task": task.to_dict()
    }, 200


@task_bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    task = get_record_by_id(Task, id)
    request_body = request.get_json()
    task.update(request_body)

    print(task.to_dict())
    db.session.commit()
    
    return {
        "task": task.to_dict()
    }
    
@task_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = get_record_by_id(Task, id)
    print(task.description)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.task_id} \"{task.title}\" successfully deleted'
    }


@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete_task(id):
    task = get_record_by_id(Task, id)
    task.completed_at = date.today()

    db.session.commit()

    return {
        "task": task.to_dict()
    }


@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(id):
    task = get_record_by_id(Task, id)
    task.completed_at = None 

    db.session.commit()

    return {
        "task": task.to_dict()
    }