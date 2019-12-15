import flask
import flask_login
from flask import abort, flash, redirect, render_template, g
from flask_login import login_required, current_user
from app import oidc

from . import home
from .. import db
from ..models import Employee
from keycloak import KeycloakAdmin
from keycloak_wrapper import user_attributes
from config import app_config

@home.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getfield('name')

        g.role = "employee"

        email = oidc.user_getfield('email')
        groups = oidc.user_getfield('groups')
        print('groups : ',app_config['KEYCLOAK_URL'])

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

@home.route('/')
def homepage():
    return render_template('home/index.html', title='PeoplePlus')


@home.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/hr/dashboard')
@oidc.require_login
@oidc.require_keycloak_role('account', 'Manager')
def hr_dashboard():
    print(oidc.user_getfield('attributes'))
    return render_template('home/hr_dashboard.html', title='Admin Dashboard')


@home.route('/profile', methods=['GET', 'POST'])
@oidc.require_login
def profile():

    return render_template('home/profilepage.html', title='Employee Profile')


@home.route('/moodle', methods=['GET', 'POST'])
@oidc.require_login
def moodle():
    print(' calling moodle')
    return render_template('home/moodle.html', title='Learning Module')