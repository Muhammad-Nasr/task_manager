from flask import Blueprint, redirect, url_for, request
from flask import render_template, request
from main.home.forms import HomeForm, HomeTaskForm

home = Blueprint('home', __name__)


# todo create home page

@home.route('/', methods=['GET', 'POST'])
@home.route('/home', methods=['GET', 'POST'])
def home_page():
    form = HomeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            task = form.task.data

            return redirect(url_for('home.home_task_page', task=task))

        return render_template("index.html", form=form)

    if request.method == 'GET':
        return render_template("index.html", form=form)


@home.route('/home-task', methods=['GET', 'POST'])
def home_task_page():
    form = HomeTaskForm()

    if request.method == "POST":
        if form.validate_on_submit():
            tasks = form.task.data
            return render_template('home_task.html', task=tasks)

    if request.method == 'GET':
        task = request.args.get('task')
        return render_template('home_task.html', form=form, task=task)










