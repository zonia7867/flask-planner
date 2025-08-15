from flask import Blueprint, render_template
from flask import request, redirect, url_for
from . import mongo
from datetime import datetime
from bson.objectid import ObjectId
from flask import jsonify
import json
from flask import session
main = Blueprint('main', __name__)  

@main.route('/')
def home():
    return render_template("home.html")

@main.route('/inbox')
def inbox():
    return render_template("inbox.html")

@main.route('/list', methods=['GET', 'POST'])
def list_page():
    if request.method == 'POST':
        title = request.form.get('title')
        space = request.form.get('space') or "General"
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        if title:
            mongo.db.tasks.insert_one({
                'title': title,
                'status': False,
                'space': space,
                'stage': "To Do",
                'created_at': datetime.utcnow(),
                'due_date': due_date
            })
        return redirect(url_for('main.list_page', space=space))

    space_filter = request.args.get('space')
    query = {'space': space_filter} if space_filter else {}
    tasks = mongo.db.tasks.find(query).sort("created_at", -1)
    return render_template("list.html", tasks=tasks, current_space=space_filter)


@main.route('/board')
def board():
    tasks = list(mongo.db.tasks.find())
    
    stages = {
        'To Do': [],
        'In Progress': [],
        'Done': []
    }

    for task in tasks:
        stage = task.get('stage', 'To Do')
        stages[stage].append(task)

    return render_template('board.html', stages=stages)

@main.route('/calendar')
def calendar():
    tasks = mongo.db.tasks.find({'due_date': {'$ne': None}})
    events = []

    for task in tasks:
        events.append({
            'title': task['title'],
            'start': task['due_date'].strftime('%Y-%m-%d'),
            'url': url_for('main.mark_done', task_id=str(task['_id']))
        })

    return render_template('calendar.html', tasks_json=json.dumps(events))

@main.route('/space/<name>', methods=['GET'])
def space(name):
    notes = list(mongo.db.notes.find({'space': name}).sort('updated_at', -1))
    return render_template("space.html", name=name, notes=notes, selected_note=None)


@main.route('/space/<name>/add', methods=['POST'])
def add_note(name):
    title = request.form.get('title')
    if title:
        mongo.db.notes.insert_one({
            'space': name,
            'title': title,
            'content': '',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
    return redirect(url_for('main.space', name=name))

@main.route('/space/<name>/note/<note_id>', methods=['GET'])
def space_note(name, note_id):
    notes = list(mongo.db.notes.find({'space': name}).sort('updated_at', -1))
    selected_note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    return render_template("space.html", name=name, notes=notes, selected_note=selected_note)

@main.route('/space/<name>/save/<note_id>', methods=['POST'])
def save_note(name, note_id):
    content = request.form.get('content')
    mongo.db.notes.update_one(
        {'_id': ObjectId(note_id)},
        {'$set': {
            'content': content,
            'updated_at': datetime.utcnow()
        }}
    )
    return redirect(url_for('main.space_note', name=name, note_id=note_id))

@main.route('/space/<name>/delete/<note_id>', methods=['POST'])
def delete_note(name, note_id):
    mongo.db.notes.delete_one({'_id': ObjectId(note_id)})
    return redirect(url_for('main.space', name=name))

@main.route('/done/<task_id>')
def mark_done(task_id):
    space = request.args.get('space')
    mongo.db.tasks.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'status': True, 'stage': 'Done'}}
    )
    return redirect(url_for('main.list_page', space=space))

@main.route('/delete/<task_id>')
def delete_task(task_id):
    space = request.args.get('space')
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('main.list_page', space=space))

@main.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    current_space = request.args.get('space')

    if request.method == 'POST':
        new_title = request.form.get('title')
        new_space = request.form.get('space') or 'General'
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        mongo.db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {
                'title': new_title,
                'space': new_space,
                'due_date': due_date
            }}
        )
        return redirect(url_for('main.list_page', space=current_space))

    return render_template('edit_task.html', task=task)

@main.route('/update_task_stage/<task_id>', methods=['POST'])
def update_task_stage(task_id):
    new_stage = request.form.get('stage')
    status = True if new_stage == 'Done' else False

    mongo.db.tasks.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'stage': new_stage, 'status': status}}
    )

    return redirect(url_for('main.board'))
