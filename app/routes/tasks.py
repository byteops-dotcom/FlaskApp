from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app import db
from app.models import Task, User

task_bp = Blueprint("task", __name__)
STATUS_ORDER = ("pending", "working", "completed")


@task_bp.before_request
def load_user():
    g.user = db.session.get(User, session["user_id"]) if "user_id" in session else None
    if "user_id" in session and g.user is None:
        session.clear()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Sign in to open your focus board.", "info")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


@task_bp.route("/")
@login_required
def view_tasks():
    tasks = Task.query.filter_by(user_id=g.user.id).order_by(Task.created_at.desc()).all()
    counts = {status: sum(task.status == status for task in tasks) for status in STATUS_ORDER}
    return render_template("tasks.html", tasks=tasks, counts=counts, total=len(tasks))


@task_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Give your next task a title first.", "error")
    elif len(title) > 120:
        flash("Keep task titles under 120 characters.", "error")
    else:
        db.session.add(Task(title=title, user_id=g.user.id))
        db.session.commit()
        flash("Task added to your board.", "success")
    return redirect(url_for("task.view_tasks"))


@task_bp.route("/update/<int:task_id>", methods=["POST"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.user.id).first_or_404()
    title = request.form.get("title", "").strip()
    if not title:
        flash("A task needs a title before it can be forged.", "error")
    elif len(title) > 120:
        flash("Keep task titles under 120 characters.", "error")
    else:
        task.title = title
        db.session.commit()
        flash("Task updated.", "success")
    return redirect(url_for("task.view_tasks"))


@task_bp.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.user.id).first_or_404()
    task.status = STATUS_ORDER[(STATUS_ORDER.index(task.status) + 1) % len(STATUS_ORDER)]
    db.session.commit()
    return redirect(url_for("task.view_tasks"))


@task_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task removed from the board.", "info")
    return redirect(url_for("task.view_tasks"))


@task_bp.route("/clear", methods=["POST"])
@login_required
def clear_tasks():
    Task.query.filter_by(user_id=g.user.id).delete()
    db.session.commit()
    flash("Your board is clear. Enjoy the breathing room.", "info")
    return redirect(url_for("task.view_tasks"))
