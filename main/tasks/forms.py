from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,DateField, BooleanField



class TaskForm(FlaskForm):
    task_name = StringField(render_kw={'autofocus': True, 'class': 'task-form',
                                  'placeholder': 'Type Here, eg: I want to do my exercise at.....'})

    task_description = TextAreaField(render_kw={'placeholder': 'Describe your task.........'})
    task_date = DateField(label='Which date is your favorite?', format='%Y-%m-%d')
    submit = SubmitField(label='Save My Task')



class CheckForm(FlaskForm):
    check_box= BooleanField(label='Done', default=False)



