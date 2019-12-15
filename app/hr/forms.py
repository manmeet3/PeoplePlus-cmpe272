from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from ..models import Department, Role, Grade


# class DepartmentForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     description = StringField('Description', validators=[DataRequired()])
#     submit = SubmitField('Submit')


# class RoleForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     description = StringField('Description', validators=[DataRequired()])
#     submit = SubmitField('Submit')


# class GradeForm(FlaskForm):
#     paygrade = StringField('Pay Grade', validators=[DataRequired()])
#     amount = StringField('Amount', validators=[DataRequired()])
#     submit = SubmitField('Submit')


# class EmployeeAssignForm(FlaskForm):
#     department = QuerySelectField(query_factory=lambda: Department.query.all(),
#                                   get_label="name")
#     role = QuerySelectField(query_factory=lambda: Role.query.all(),
#                             get_label="name")
#     grade = QuerySelectField(query_factory=lambda: Grade.query.all(),
#                             get_label="paygrade")
#     submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
    emp_no = StringField('id')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    hire_date = StringField('Hire Date', validators=[DataRequired()])
    birth_date = StringField('Birth Date', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Save')
