from flask import abort, flash, redirect, render_template, url_for, request, g
from flask_login import current_user, login_required
from datetime import date

from keycloak import KeycloakAdmin

from . import manager
#from forms import DepartmentForm, RoleForm, EmployeeAssignForm, GradeForm
from .. import db
from flask_paginate import Pagination, get_page_args
from ..models import Department, DeptEmp, DeptMgr, Employee, Salary, Title
from app import oidc
from datetime import datetime, timedelta
from .. import db
from ..models import Department, DeptEmp, DeptMgr, Employee, Salary, Title
from app import oidc
from datetime import datetime, timedelta
import httplib2
from config import app_config


@manager.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getfield('name')

        g.role = "Manager"

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
                print(user['attributes']['emp_id'])
                print(user['attributes']['role'][0])
                g.role = user['attributes']['role'][0]
                g.empId = user['attributes']['emp_id'][0]



    else:
        g.user = None




@manager.route('/employees/view', methods=['GET'])
@oidc.require_keycloak_role('account', 'Manager')
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
    deptManager = DeptMgr.query.filter_by(dept_no=deptEmp.department.dept_no).all()
    print('manager emp no: ', deptManager[0].emp_no)
    manager = Employee.query.get(deptManager[0].emp_no)
    print(manager)
    manager_name = manager.first_name + " " + manager.last_name
    print('salary : ',salary.salary)
    print('title: ',title.title)
    emp = [employee.emp_no, employee.first_name,employee.last_name,employee.hire_date, employee.birth_date,employee.gender, title.title, salary.salary,deptEmp.department.dept_name,manager_name]



    return render_template('manager/employees/view_employee.html', action="Edit",
                           employee=emp,
                           title="View Employees")

@manager.route('/deptEmployees', methods=['GET'])
@oidc.require_keycloak_role('account', 'Manager')
@oidc.require_login
def list_employee_dept():
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = (page - 1) * per_page

    #page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')

    empId = request.args.get('empId')
    print('line 97 : ',empId)
    deptEmp = DeptEmp.query.filter_by(emp_no=empId).first()
    print('line 99 : ',deptEmp.dept_no)
    dept_no = deptEmp.dept_no
    department = Department.query.get_or_404(dept_no)
    print(department)
    #employees_id = DeptEmp.query.get_or_404(department)

    #employees_id = DeptEmp.query.get(department)
    today = str(date.today())

    emp_count = DeptEmp.query.filter(DeptEmp.dept_no == dept_no).\
                    filter(DeptEmp.to_date >= today).count()

    deptEmp = DeptEmp.query.filter(DeptEmp.dept_no == dept_no).\
                    filter(DeptEmp.to_date >= today).paginate(page=page, per_page=per_page).items
    print('dept num : ',dept_no)
    deptManager = DeptMgr.query.filter_by(dept_no=dept_no).all()
    print('manager emp no: ',deptManager)
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

    print('line 110:', len(employee))
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
    return render_template('manager/employees/employees.html', page=page,
                           per_page=per_page,
                           employees=employees, title="List Employees", pagination=pagination)