from flask import abort, flash, redirect, render_template, url_for, request, g
from flask_login import current_user, login_required
from datetime import date

from keycloak import KeycloakAdmin

from config import app_config
from . import employee
#from forms import DepartmentForm, RoleForm, EmployeeAssignForm, GradeForm
from .. import db
from ..models import Department, DeptEmp, DeptMgr, Employee, Salary, Title
from app import oidc
from datetime import datetime, timedelta

@employee.before_request
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



@employee.route('/view', methods=['GET'])
@oidc.require_keycloak_role('account', 'employee')
@oidc.require_login
def view_employee():
    """
    Edit a department
    """
    today=str(date.today())
    now = datetime.now()

    add_employee = False
    empId = request.args.get('empId')
    print('g.emp_id ',g.empId)
    employee = Employee.query.get(empId)

    print(employee.first_name)
    salary = employee.salary.filter(Salary.to_date >= today).first()
    title = employee.title.filter(Title.to_date >= today).first()
    deptEmp = DeptEmp.query.filter_by(emp_no=employee.emp_no).first()
    #depts = employee.dept.all()

    print('salary : ',salary.salary)
    print('title: ',title.title)
    emp = [employee.emp_no, employee.first_name,employee.last_name,employee.hire_date, employee.birth_date, title.title, salary.salary,deptEmp.department.dept_name]



    return render_template('employee/view_employee.html', action="Edit",
                           employee=emp,
                           title="Edit Employee")
