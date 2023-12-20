from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ToDoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')
