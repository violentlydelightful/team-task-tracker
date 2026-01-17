#!/usr/bin/env python3
"""
Team Task Tracker - Internal dashboard for managing team workload
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Models
class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(100))
    avatar_color = db.Column(db.String(20), default="#667eea")
    tasks = db.relationship("Task", backref="assignee", lazy=True)

    @property
    def active_tasks(self):
        return [t for t in self.tasks if t.status != "done"]

    @property
    def workload_score(self):
        score = 0
        for task in self.active_tasks:
            if task.priority == "high":
                score += 3
            elif task.priority == "medium":
                score += 2
            else:
                score += 1
        return score


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="todo")  # todo, in_progress, review, done
    priority = db.Column(db.String(20), default="medium")  # low, medium, high
    due_date = db.Column(db.Date)
    project = db.Column(db.String(100))
    assignee_id = db.Column(db.Integer, db.ForeignKey("team_member.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_overdue(self):
        if self.due_date and self.status != "done":
            return self.due_date < datetime.now().date()
        return False

    @property
    def days_until_due(self):
        if self.due_date:
            delta = self.due_date - datetime.now().date()
            return delta.days
        return None


# Routes
@app.route("/")
def dashboard():
    members = TeamMember.query.all()
    tasks = Task.query.order_by(Task.updated_at.desc()).all()

    # Calculate stats
    stats = {
        "total": len(tasks),
        "todo": len([t for t in tasks if t.status == "todo"]),
        "in_progress": len([t for t in tasks if t.status == "in_progress"]),
        "review": len([t for t in tasks if t.status == "review"]),
        "done": len([t for t in tasks if t.status == "done"]),
        "overdue": len([t for t in tasks if t.is_overdue]),
        "high_priority": len([t for t in tasks if t.priority == "high" and t.status != "done"]),
    }

    # Get unique projects
    projects = list(set(t.project for t in tasks if t.project))

    return render_template(
        "dashboard.html", members=members, tasks=tasks, stats=stats, projects=projects
    )


@app.route("/board")
def board():
    members = TeamMember.query.all()
    tasks = Task.query.all()

    board_data = {
        "todo": [t for t in tasks if t.status == "todo"],
        "in_progress": [t for t in tasks if t.status == "in_progress"],
        "review": [t for t in tasks if t.status == "review"],
        "done": [t for t in tasks if t.status == "done"],
    }

    return render_template("board.html", board=board_data, members=members)


@app.route("/team")
def team():
    members = TeamMember.query.all()
    return render_template("team.html", members=members)


@app.route("/api/task", methods=["POST"])
def create_task():
    data = request.get_json()

    due_date = None
    if data.get("due_date"):
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "todo"),
        priority=data.get("priority", "medium"),
        due_date=due_date,
        project=data.get("project"),
        assignee_id=data.get("assignee_id"),
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({"success": True, "task_id": task.id})


@app.route("/api/task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "priority" in data:
        task.priority = data["priority"]
    if "project" in data:
        task.project = data["project"]
    if "assignee_id" in data:
        task.assignee_id = data["assignee_id"] or None
    if "due_date" in data:
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data["due_date"] else None

    db.session.commit()
    return jsonify({"success": True})


@app.route("/api/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True})


@app.route("/api/member", methods=["POST"])
def create_member():
    data = request.get_json()
    member = TeamMember(
        name=data["name"],
        email=data.get("email"),
        role=data.get("role"),
        avatar_color=data.get("avatar_color", "#667eea"),
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({"success": True, "member_id": member.id})


@app.route("/api/stats")
def api_stats():
    tasks = Task.query.all()
    members = TeamMember.query.all()

    return jsonify(
        {
            "tasks": {
                "total": len(tasks),
                "by_status": {
                    "todo": len([t for t in tasks if t.status == "todo"]),
                    "in_progress": len([t for t in tasks if t.status == "in_progress"]),
                    "review": len([t for t in tasks if t.status == "review"]),
                    "done": len([t for t in tasks if t.status == "done"]),
                },
                "by_priority": {
                    "high": len([t for t in tasks if t.priority == "high"]),
                    "medium": len([t for t in tasks if t.priority == "medium"]),
                    "low": len([t for t in tasks if t.priority == "low"]),
                },
            },
            "team": {
                "total": len(members),
                "workload": [{"name": m.name, "score": m.workload_score} for m in members],
            },
        }
    )


@app.route("/seed")
def seed_demo_data():
    """Seed database with demo data."""
    # Clear existing
    Task.query.delete()
    TeamMember.query.delete()

    # Create team members
    members_data = [
        {"name": "Alex Chen", "role": "Developer", "avatar_color": "#667eea"},
        {"name": "Sarah Kim", "role": "Designer", "avatar_color": "#48bb78"},
        {"name": "Mike Johnson", "role": "Developer", "avatar_color": "#ed8936"},
        {"name": "Lisa Park", "role": "Project Manager", "avatar_color": "#ed64a6"},
    ]

    members = []
    for m in members_data:
        member = TeamMember(**m)
        db.session.add(member)
        members.append(member)

    db.session.flush()

    # Create tasks
    today = datetime.now().date()
    tasks_data = [
        {"title": "Design new dashboard layout", "project": "Dashboard Redesign", "priority": "high", "status": "in_progress", "assignee": 1, "due": 3},
        {"title": "Implement user authentication", "project": "Auth System", "priority": "high", "status": "review", "assignee": 0, "due": 1},
        {"title": "Write API documentation", "project": "Auth System", "priority": "medium", "status": "todo", "assignee": 0, "due": 7},
        {"title": "Create onboarding flow mockups", "project": "Onboarding", "priority": "medium", "status": "done", "assignee": 1, "due": -2},
        {"title": "Fix login page responsiveness", "project": "Auth System", "priority": "low", "status": "todo", "assignee": 2, "due": 5},
        {"title": "Set up CI/CD pipeline", "project": "Infrastructure", "priority": "high", "status": "in_progress", "assignee": 2, "due": 2},
        {"title": "Review Q4 roadmap", "project": "Planning", "priority": "medium", "status": "todo", "assignee": 3, "due": 4},
        {"title": "User research interviews", "project": "Onboarding", "priority": "high", "status": "todo", "assignee": 1, "due": -1},
        {"title": "Database optimization", "project": "Infrastructure", "priority": "medium", "status": "in_progress", "assignee": 0, "due": 6},
        {"title": "Update team wiki", "project": "Documentation", "priority": "low", "status": "done", "assignee": 3, "due": -3},
    ]

    for t in tasks_data:
        task = Task(
            title=t["title"],
            project=t["project"],
            priority=t["priority"],
            status=t["status"],
            assignee_id=members[t["assignee"]].id,
            due_date=today + timedelta(days=t["due"]),
        )
        db.session.add(task)

    db.session.commit()
    return redirect(url_for("dashboard"))


# Initialize database
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Team Task Tracker")
    print("=" * 50)
    print("\n  Starting server at: http://localhost:5002")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5002)
