from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.routes_helper import *
from app.models.goal import Goal
from app.models.task import Task


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as err:
        error_message(f"Invalid data", 400)
    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()
    }, 201

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goal_query = Goal.query

    sort = request.args.get("sort")
    if sort == "desc":
        goal_query = goal_query.order_by(Goal.title.desc())
    elif sort == "asc":
        goal_query = goal_query.order_by(Goal.title.asc())

    goals = goal_query.all()
    goal_response = [goal.to_dict() for goal in goals]
    return jsonify(goal_response), 200

@goal_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = get_record_by_id(Goal, id)
    return {
        "goal": goal.to_dict()
    }, 200


@goal_bp.route("/<id>", methods=["PUT"])
def update_one_goal(id):
    goal = get_record_by_id(Goal, id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()
    
    return {
        "goal": goal.to_dict()
    }
    
@goal_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = get_record_by_id(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }

@goal_bp.route("/<id>/tasks", methods=["POST"])
def add_task_to_goal(id):
    goal = get_record_by_id(Goal, id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = get_record_by_id(Task, task_id)
        task.goal_id = id
        task.goal = goal

    db.session.commit()

    task_ids = []
    for task in goal.tasks:
        task_ids.append(task.task_id)

    return {
        'id': goal.goal_id,
        "task_ids": task_ids
    }

@goal_bp.route("/<id>/tasks", methods=["GET"])
def read_tasks_of_goal(id):
    goal = get_record_by_id(Goal, id)
    task_list = [task.to_dict() for task in goal.tasks]
    # print(task_list)
    
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = task_list

    return jsonify(goal_dict)


