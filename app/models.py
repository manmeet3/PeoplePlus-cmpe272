'''
@ Manmeet Singh
@ Nov 26, 2019
@ Description: The below classes serve as the model layer for ORM mapping from MySQL database to
python objects.
'''

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, lazyload
from sqlalchemy.ext.declarative import declarative_base

from app import db

'''
Map Department Table
'''
class Department(db.Model):
    __tablename__ = 'departments'

    dept_no=db.Column(db.CHAR(4), primary_key=True)
    dept_name=db.Column(db.String(40), unique=True)
    dept_employees=relationship("DeptEmp", back_populates="department", lazy="dynamic")
    dept_managers=relationship("DeptMgr", back_populates="department", lazy="dynamic")

    def __repr__(self):
        return '{}'.format(self.dept_name)

'''
Map Department and Employee relation table
'''
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

'''
The below table maps Departments with their manager's employee id
'''
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

'''
The below table maps Employee to a python object
'''
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

'''
The below table maps emp id with a salary value
'''
class Salary(db.Model):
    __tablename__ = 'salaries'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    salary=db.Column(db.Integer)
    from_date=db.Column(db.Date, primary_key=True)
    to_date=db.Column(db.Date)
    employee=relationship("Employee", back_populates="salary")
    def __repr__(self):
        return '{}'.format(self.salary)

'''
The below maps the title of an employee with emp id
'''
class Title(db.Model):
    __tablename__ = 'titles'

    emp_no=db.Column(db.Integer, ForeignKey('employees.emp_no'), primary_key=True)
    title=db.Column(db.String(50), primary_key=True)
    from_date=db.Column(db.Date, primary_key=True)
    to_date=db.Column(db.Date)
    employee=relationship("Employee", back_populates="title")
    def __repr__(self):
        return '{}'.format(self.title)
