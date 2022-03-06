from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField



class HomeForm(FlaskForm):
    task = StringField(render_kw={'autofocus': True, 'class': 'task-form',
                                  'placeholder': 'Type Here, eg: I have to walk for .....'})
    submit= SubmitField(render_kw={'class': 'task-submit'})



class HomeTaskForm(FlaskForm):
    task = StringField(render_kw={'autofocus': True,
                                  'placeholder': 'Write your next task here... .....'})
    check_box = BooleanField(label='Done', default=False)
    task_date = DateField(label='Which date is your favorite?', format='%Y-%m-%d')

    submit = SubmitField(label='Save')