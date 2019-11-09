#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
from flask_sqlalchemy import SQLAlchemy

cwd = os.getcwd()

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    cwd = sys._MEIPASS
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)








app.secret_key = 'yusserbaby'
app.debug = True

print(cwd)
from config import *
# app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://{}:{}@{}/{}'.format(DATABASR_USERNAME ,DATABASR_PASSWORD ,DATABASR_SERVER ,DATABASR_NAME)
# app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+cwd+'/data.db' 
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get("CLEARDB_DATABASE_URL")[:-15]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from db_models import *
db.create_all()






from routes.login_blueprint import login_blueprint, User, users
app.register_blueprint(login_blueprint,url_prefix='/')
from routes.employee_blueprint import employee_blueprint
app.register_blueprint(employee_blueprint,url_prefix='/')
from routes.employee_hours_blueprint import employee_hours_blueprint
app.register_blueprint(employee_hours_blueprint,url_prefix='/')
from routes.employee_advance_blueprint import employee_advance_blueprint
app.register_blueprint(employee_advance_blueprint,url_prefix='/')
from routes.employee_salary_blueprint import employee_salary_blueprint
app.register_blueprint(employee_salary_blueprint,url_prefix='/')




@app.route('/admin')
def show_admin(name=None):

	return render_template('admin/admin.html', name=name)


@app.route('/user')
def show_user(name=None):

	return render_template('user/index.html', name=name)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):

	return render_template('hello.html', name=name)












# login manager
import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[username]['password']

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/admin/login')


    


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, threaded=False)