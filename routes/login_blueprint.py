from flask import Flask, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
from flask import  jsonify
import flask_login


login_blueprint = Blueprint("login_blueprint",__name__)

###########      login



# Our mock database.
users = {'admin': {'password': 'admin'}}


###########      login



class User(flask_login.UserMixin):
    pass





@login_blueprint.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login/login.html')

    username = request.form['username']
    if username in users:
	    if request.form['password'] == users[username]['password']:
	        user = User()
	        user.id = username
	        flask_login.login_user(user)
	        return redirect('/admin')

    return redirect('/admin/login')




@login_blueprint.route('/admin/logout')
def logout():
    flask_login.logout_user()
    return redirect('/admin/login')




@login_blueprint.route('/api/login', methods=['POST'])
def api_login():
    response = {"status":"fail"}

    data = request.form
    if not data:
        print("args")
        data = request.args

    if not data:
        print("json")
        data = request.json

    username = data.get('username')
    if username in users:
        if data.get('password') == users[username]['password']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            response['status'] = 'success'

    response = jsonify(response)
    return response




@login_blueprint.route('/api/logout')
def api_logout():
    response = {"status":"success"}
    flask_login.logout_user()
    response = jsonify(response)
    return response



