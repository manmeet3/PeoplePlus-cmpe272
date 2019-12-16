import codecs

from flask import abort, flash, redirect, render_template, url_for, request, g
from flask_login import current_user, login_required
from datetime import date

from flask_paginate import Pagination, get_page_args
from pkg_resources import resource_stream
from sqlalchemy.dialects.mysql import json
from keycloak_wrapper import access_token
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin
from keycloak_wrapper import user_attributes

from . import hr
from .forms import EmployeeForm
from .. import db
from ..models import Department, DeptEmp, DeptMgr, Employee, Salary, Title
from app import oidc
from datetime import datetime, timedelta
import httplib2
from config import app_config


#from keycloak.aio.realm import KeycloakRealm

@hr.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getfield('name')

        g.role = "hr"

        email = oidc.user_getfield('email')
        groups = oidc.user_getfield('groups')
        print('groups : ',groups)

        keycloak_admin = KeycloakAdmin(server_url=app_config['KEYCLOAK_URL'],
                                       username=app_config['USERNAME'],
                                       password=app_config['PASSWORD'],
                                       realm_name=app_config['REALM_NAME'],
                                       verify=True)
        users = keycloak_admin.get_users({})
        #print(users)
        for user in users:
            print(user)
            if(email.strip().lower() == user['email'].strip().lower()):
                print(user['attributes'])
                print(user['attributes']['emp_id'])
                print(user['attributes']['role'][0])
                print(g)
                g.role = user['attributes']['role'][0]
                g.empId = user['attributes']['emp_id'][0]
                break

    else:
        g.user = None


@hr.route('/departments', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def list_departments():
    #create_emp_keycloak()
    print('department called ')
    today=str(date.today())
    departments = Department.query.all()
    #departments.dept_employees.all() #filter(DeptEmp.to_date >= today)
    depts=[]
    for dept in departments:
        dept_employees=dept.dept_employees.filter(DeptEmp.to_date >= today).count()
        #dept_employees = DeptEmp.query.filter(DeptEmp.dept_no==dept.dept_no).all()
        print('length: ',dept_employees)

        thisdept=[dept.dept_no, dept.dept_name, dept_employees]
        depts.append(thisdept)

    return render_template('hr/departments/departments.html',
                           departments=depts, title="Departments")


@hr.route('/deptEmployees', methods=['GET'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def list_employee_dept():
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = (page - 1) * per_page

    #page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')

    departmentName = request.args.get('department')
    department = Department.query.get_or_404(departmentName)
    print(department)
    #employees_id = DeptEmp.query.get_or_404(department)

    #employees_id = DeptEmp.query.get(department)
    today = str(date.today())

    emp_count = DeptEmp.query.filter(DeptEmp.dept_no == departmentName).\
                    filter(DeptEmp.to_date >= today).count()

    deptEmp = DeptEmp.query.filter(DeptEmp.dept_no == departmentName).\
                    filter(DeptEmp.to_date >= today).paginate(page=page, per_page=per_page).items
    deptManager = DeptMgr.query.filter_by(dept_no=departmentName).all()
    print('manager emp no: ',deptManager[0].emp_no)
    manager = Employee.query.get(deptManager[0].emp_no)
    print(manager)
    manager_name = manager.first_name+" "+manager.last_name
    print(manager_name)

    employees = []


    print('employee ids : ',len(deptEmp))
    emp_ids = []
    for i in deptEmp:
        #print(i.emp_no)
        emp_ids.append(int(i.emp_no))
    print('line 87:',emp_ids[0])

    print('page :',page);
    print('per_page: ',per_page) #.filter(Salary.to_date >= today) /\ .paginate(page=page, per_page=per_page).items
    salary = Salary.query.filter(Salary.emp_no.in_(emp_ids)).filter(Salary.to_date >= today).all()
    print('line 93: salary ',len(salary)) #.filter(Title.to_date >= today),.paginate(page=page, per_page=per_page).items
    title = Title.query.filter(Title.emp_no.in_(emp_ids)).filter(Title.to_date >= today).all()
    print('line 95: title ',len(title))
    #print(salary[0].emp_no, salary[0].salary)
    emp_ids = []

    if(len(salary) < len(title)):
        for s in salary:
            emp_ids.append(int(s.emp_no))

        employee = Employee.query.filter(Employee.emp_no.in_(emp_ids)).all() #.paginate(page=page, per_page=per_page).items#.all()  # emp_no.in(emp_id))
    else:
        for s in title:
            emp_ids.append(int(s.emp_no))

        employee = Employee.query.filter(Employee.emp_no.in_(emp_ids)).all() #.paginate(page=page, per_page=per_page).items#.all()  # emp_no.in(emp_id))

    #print(employee[0].first_name,employee[0].last_name,salary[0], title[0])
    print(len(employee), len(salary), len(title), department.dept_name)
    for j in range(0, len(employee)-1):
        #salary = emp.salary.filter(Salary.to_date >= today).all()
        #title = emp.title.filter(Title.to_date >= today).all()
        #print(j)
        emp1 = [employee[j].emp_no,employee[j].first_name, employee[j].last_name, employee[j].gender, salary[j], title[j],department.dept_name, manager_name]
        employees.append(emp1)

    search = False

    #pagination = Pagination(page=page, per_page=per_page, total=500000)
    pagination = Pagination(page=page, per_page=per_page, total=emp_count,
                            css_framework='bootstrap4')
    return render_template('hr/employees/employees.html', page=page,
                           per_page=per_page,
                           employees=employees, title="List Employees", pagination=pagination)


@hr.route('/department/view', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def view_department():
    today=str(date.today())
    departmentName = request.args.get('department')
    print(departmentName)
    department = Department.query.get_or_404(departmentName)
    print(department)
    #form = DepartmentForm(obj=department)


    return render_template('hr/departments/department.html',
                           department=department, title="View Department")

@hr.route('/employee/create/', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def create_employee():
    add_employee = True
    today=str(date.today())

    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(first_name=form.first_name.data,last_name=form.last_name.data,
                            birth_date=form.birth_date.data,gender=form.gender.data,
                            hire_date=form.hire_date.data)
        db.session.add(employee)
        db.session.flush()
        emp_no = employee.emp_no
        print(employee.emp_no)
        dept = DeptEmp(emp_no = emp_no, dept_no=form.department.data,from_date=form.hire_date.data,to_date='9999-01-01')
        salary = Salary(emp_no = emp_no, salary=form.salary.data,from_date=form.hire_date.data,to_date='9999-01-01')
        title = Title(emp_no = emp_no, title=form.title.data,from_date=form.hire_date.data,to_date='9999-01-01')

        db.session.add(dept)
        db.session.add(salary)
        db.session.add(title)

        db.session.flush()
        db.session.commit()
        employee = [emp_no,employee.first_name, employee.last_name, employee.first_name+"."+employee.last_name+"@peopleplus.org"]
        create_emp_keycloak(employee)
        return redirect(url_for('hr.view_employee', id=emp_no))



    #load department template
    return render_template('hr/employees/employee.html', action="Add",
                               add_employee=add_employee, form=form,
                               title="Add Employee")


@hr.route('/employee/edit/', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def edit_employee():
    """
    Edit a department
    """
    today=str(date.today())
    now = datetime.now()

    add_employee = False
    emp_id = request.args.get('id')
    employee = Employee.query.get(emp_id)
    form = EmployeeForm(obj=employee)
    form.emp_no.data = employee.emp_no

    print(employee.first_name)

    print('edit employee : ',id)

    if form.validate_on_submit():
        #employee.last_name = form.last_name.data

        employee = Employee.query.get(form.emp_no.data)
        salary = employee.salary.filter(Salary.to_date >= today).first()
        title = employee.title.filter(Title.to_date >= today).first()
        deptEmp = DeptEmp.query.filter_by(emp_no=employee.emp_no).first()
        employee.last_name = form.last_name.data

        deptEmp.dept_no = form.department.data
        salary.salary = form.salary.data
        title.title = form.title.data

        db.session.commit()
        flash('You have successfully edited the Employee information.')
        return redirect(url_for('hr.list_employee_dept', department=form.department.data))

    form.first_name.data = employee.first_name
    form.last_name.data = employee.last_name
    form.hire_date.data = employee.hire_date
    form.gender.data = employee.gender
    form.birth_date.data = employee.birth_date
    salary = employee.salary.filter(Salary.to_date >= today).first()
    title = employee.title.filter(Title.to_date >= today).first()
    deptEmp = DeptEmp.query.filter_by(emp_no=employee.emp_no).first()
    #depts = employee.dept.all()
    form.department.data = deptEmp.dept_no

    print('dept: ',deptEmp.dept_no)
    form.salary.data = salary.salary
    form.title.data = title.title
    print('salary : ',salary.salary)
    print('title: ',title.title)



    return render_template('hr/employees/employee.html', action="Edit",
                           add_employee=add_employee, form=form,employee=employee,
                           title="Edit Employee")

@hr.route('/employees/delete', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def delete_employee():
    print('id: ',request.args.get('id'))
    emp_id = request.args.get('id')
    employee = Employee.query.get(emp_id)
    today=str(date.today())
    salary = employee.salary.filter(Salary.to_date >= today).first()
    title = employee.title.filter(Title.to_date >= today).first()
    deptEmp = DeptEmp.query.filter_by(emp_no=employee.emp_no).first()
    dept_no = deptEmp.dept_no
    db.session.delete(salary)
    db.session.delete(title)
    # db.session.delete(deptEmp)
    db.session.delete(deptEmp)
    #db.session.delete(employee)
    db.session.commit()



    return redirect(url_for('hr.list_employee_dept', department=dept_no))

@hr.route('/employees/view', methods=['GET', 'POST'])
@oidc.require_keycloak_role('account', 'hr')
@oidc.require_login
def view_employee():
    """
    Edit a department
    """
    today=str(date.today())
    now = datetime.now()

    add_employee = False
    emp_id = request.args.get('empId')
    employee = Employee.query.get(emp_id)

    print(employee.first_name)
    salary = employee.salary.filter(Salary.to_date >= today).first()
    title = employee.title.filter(Title.to_date >= today).first()
    deptEmp = DeptEmp.query.filter_by(emp_no=employee.emp_no).first()
    #depts = employee.dept.all()
    deptManager = DeptMgr.query.filter_by(dept_no=deptEmp.dept_no).all()
    print('manager emp no: ', deptManager[0].emp_no)
    manager = Employee.query.get(deptManager[0].emp_no)
    print(manager.first_name)

    print('salary : ',salary.salary)
    print('title: ',title.title)
    emp = [employee.emp_no, employee.first_name,employee.last_name,employee.hire_date, employee.birth_date,employee.gender,
            title.title, salary.salary,deptEmp.department.dept_name,manager.first_name+" "+manager.last_name]



    return render_template('hr/employees/view_employee.html', action="Edit",
                           employee=emp,
                           title="Edit Employee")

"""
Create keycloak account for new employee
"""
def create_emp_keycloak(employee):
    headers = {'Content-type': 'application/json'}
    print('config : ',app_config['CLIENT_SECRET'])
    keycloak_admin = KeycloakAdmin(server_url=app_config['KEYCLOAK_URL'],
                                   username=app_config['USERNAME'],
                                   password=app_config['PASSWORD'],
                                   realm_name=app_config['REALM_NAME'],
                                   verify=True)
    users = keycloak_admin.get_users({})
    print(users[0]['attributes']['emp_id'])

    #   attrs = user_attributes(app_config['KEYCLOAK_URL'], app_config['REALM_NAME'], app_config['KEYCLOAK_URL'], token, "Jeyasri")
    #   print(attrs)
    new_user = keycloak_admin.create_user({"email": employee[3],
                                           "username": employee[1],
                                           "enabled": True,
                                           "firstName": employee[1],
                                           "lastName": employee[2],
                                           "credentials": [{"value": "welcome123","type": "password",}],
                                           "attributes": {"emp_id": employee[0]}})
 