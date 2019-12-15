'''
@ Manmeet Singh
@ Nov 26, 2019
@ Cmpe 272 db mapping
'''

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, lazyload
from sqlalchemy.ext.declarative import declarative_base

from app import db

class Department(db.Model):
    __tablename__ = 'departments'

    dept_no=db.Column(db.CHAR(4), primary_key=True)
    dept_name=db.Column(db.String(40), unique=True)
    dept_employees=relationship("DeptEmp", back_populates="department", lazy="dynamic")
    dept_managers=relationship("DeptMgr", back_populates="department", lazy="dynamic")

    def __repr__(self):
        return '{}'.format(self.dept_name)

class DeptEmp(db.Model):
    __tablename__ = 'dept_emp'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no',ondelete='CASCADE'),primary_key=True)
    dept_no=db.Column(db.CHAR(4), ForeignKey('departments.dept_no'))
    from_date=db.Column(db.Date)
    to_date=db.Column(db.Date)
    department = relationship("Department", back_populates="dept_employees")
    employee = relationship("Employee")    
    def __repr__(self):
        return '{}'.format(self.emp_no)

class DeptMgr(db.Model):
    __tablename__ = 'dept_manager'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no',ondelete='CASCADE'), primary_key=True)
    dept_no=Column(db.CHAR(4), ForeignKey('departments.dept_no'))
    from_date=db.Column(db.Date)
    to_date=db.Column(db.Date)
    department = relationship("Department", back_populates="dept_managers")
    manager_emp = relationship("Employee")
    def __repr__(self):
        return '{}'.format(self.emp_no)

class Employee(db.Model):
    __tablename__ = 'employees'

    emp_no=db.Column(db.Integer, primary_key=True, autoincrement=True)
    birth_date=db.Column(db.Date)
    first_name=db.Column(db.String(14))
    last_name=db.Column(db.String(16))
    gender=db.Column(db.Enum("M", "F"))
    hire_date=db.Column(db.Date)
    salary=relationship("Salary", lazy="dynamic")
    title=relationship("Title", lazy="dynamic")
    dept=relationship("DeptEmp", back_populates="employee", lazy="dynamic")

    def __repr__(self):
        return '<Employee: {}>'.format(self.first_name)

class Salary(db.Model):
    __tablename__ = 'salaries'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    salary=db.Column(db.Integer)
    from_date=db.Column(db.Date, primary_key=True)
    to_date=db.Column(db.Date)
    employee=relationship("Employee", back_populates="salary")
    def __repr__(self):
        return '{}'.format(self.salary)

class Title(db.Model):
    __tablename__ = 'titles'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    title=db.Column(db.String(50), primary_key=True)
    from_date=db.Column(db.Date, primary_key=True)
    to_date=db.Column(db.Date)
    employee=relationship("Employee", back_populates="title")
    def __repr__(self):
        return '{}'.format(self.title)

# ===============================================================

# class Employee(UserMixin, db.Model):
#     """
#     Create an Employee table
#     """

#     # Ensures table will be named in plural and not in singular
#     # as is the name of the model
#     __tablename__ = 'employees'

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(60), index=True, unique=True)
#     username = db.Column(db.String(60), index=True, unique=True)
#     first_name = db.Column(db.String(60), index=True)
#     last_name = db.Column(db.String(60), index=True)
#     password_hash = db.Column(db.String(128))
#     department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#     grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))
#     is_admin = db.Column(db.Boolean, default=False)

#     @property
#     def password(self):
#         """
#         Prevent pasword from being accessed
#         """
#         raise AttributeError('password is not a readable attribute.')

#     @password.setter
#     def password(self, password):
#         """
#         Set password to a hashed password
#         """
#         self.password_hash = generate_password_hash(password)

#     def verifypassword(self, password):
#         """
#         Check if hashed password matches actual password
#         """
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return '<Employee: {}>'.format(self.username)


# # Set up user_loader
# @login_manager.user_loader
# def load_user(user_id):
#     return Employee.query.get(int(user_id))


# class Department(db.Model):
#     """
#     Create a Department table
#     """

#     __tablename__ = 'departments'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='department',
#                                 lazy='dynamic')

#     def __repr__(self):
#         return '{}'.format(self.name)


# class Role(db.Model):
#     """
#     Create a Role table
#     """

#     __tablename__ = 'roles'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='role',
#                                 lazy='dynamic')

#     def __repr__(self):
#         return '{}'.format(self.name)


# class Grade(db.Model):
#     """
#     Create a Pay Grade table
#     """

#     __tablename__ = 'grades'

#     id = db.Column(db.Integer, primary_key=True)
#     paygrade = db.Column(db.String(60), unique=True)
#     amount = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='grade',
#                                 lazy='dynamic')

#     def __repr__(self):
#         return '{}'.format(self.paygrade)
