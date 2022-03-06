from flask import Blueprint, session
from main import db
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from main.tasks.forms import TaskForm, CheckForm
from main.dbmodel import Tasks


tasks = Blueprint('tasks', __name__)


@tasks.route('/task', methods=['GET', 'POST'])

def task_page():
    form = TaskForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            user_task = Tasks(

                    description=form.task_description.data,
                    date='2020/02/15',
                    user_id=current_user.id
                )

            db.session.add(user_task)
            db.session.commit()

            flash('congratulation, your task added successfully!')
            return redirect(url_for('home.home_page'))
        else:
            flash(message=f'the erros {form.errors}')
            return render_template('task.html', form=form)

    elif request.method == 'GET':

        return render_template('task.html', form=form)



@tasks.route('/my-tasks', methods=['GET', 'POST'])
def personal_tasks():
    image_file = url_for('static', filename='images/' + current_user.profile_image)
    form = CheckForm()
    person_tasks = Tasks.query.filter_by(user_id=current_user.id).all()

    print(form.data)
    if form.check_box.data == False:
        print(form.check_box.data)
    else:
        print(True)

    return render_template('personal_tasks.html', form=form, person_tasks=person_tasks, image_file=image_file)






