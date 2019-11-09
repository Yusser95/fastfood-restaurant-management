from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

recipe_blueprint = Blueprint("recipe_blueprint",__name__)

from app import db



@recipe_blueprint.route('/admin/recipe/data')
@flask_login.login_required
def data():
	from db_models import RecipeModel, RecipeTagModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(RecipeModel.id),
        ColumnDT(RecipeModel.name),
        ColumnDT(RecipeTagModel.name),
        ColumnDT(RecipeModel.image),
        ColumnDT(RecipeModel.is_deleted),
        ColumnDT(RecipeModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(RecipeModel).order_by(RecipeModel.id).outerjoin(RecipeTagModel, RecipeModel.tag)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@recipe_blueprint.route("/admin/recipe/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/recipe/index.html')


@recipe_blueprint.route("/admin/recipe/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import RecipeModel
	item = RecipeModel.query.get(id)
	return render_template('admin/recipe/show.html' , item = item)

@recipe_blueprint.route("/admin/recipe/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import RecipeModel
	print("deleted " , id)
	obj = RecipeModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/recipe/index')

@recipe_blueprint.route("/admin/recipe/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import RecipeModel
	print(id)
	# edit
	if request.method == "POST":

		obj = RecipeModel.query.get(id)

		name = request.form.get('name')
		tag_id = request.form.get('tag_id')
		direction = request.form.get('direction')

		ingredients = request.form.getlist('ingredients[]')
		amounts = request.form.getlist('weights[]')
		units = request.form.getlist('values[]')

		image = ''
		if 'image' in request.files:
			file = request.files['image']
			if file:

				### claudira

				# upload_result = upload(file)
				# thumbnail_pixelate, options = cloudinary_url(
				# upload_result['public_id'],
				# format="jpg",
				# crop="fill",
				# width=350,
				# height=234,
				# radius=0,
				# gravity="center"
				# )
				# image = thumbnail_pixelate


				### manul
				filename = file.filename
				path = "public/uploads/"+name.replace(" ","_").replace("#","_").replace(".","_")+"."+filename.split(".")[-1]
				image = "/uploads/"+name.replace(" ","_").replace("#","_").replace(".","_")+"."+filename.split(".")[-1]
				file.save(path)

		obj._update(name=name , tag_id=tag_id  , direction=direction  , image=image , ingredients=ingredients , amounts=amounts , units=units  )
		db.session.commit()
		

		return redirect('/admin/recipe/index')
	# show  one row
	elif request.method == "GET":

		item = RecipeModel.query.get(id)
		return render_template('/admin/recipe/edit.html',item = item)
	return "404"


@recipe_blueprint.route("/admin/recipe/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import RecipeModel
	# edit
	if request.method == "POST":

		name = request.form.get('name')
		tag_id = request.form.get('tag_id')
		direction = request.form.get('direction')

		ingredients = request.form.getlist('ingredients[]')
		amounts = request.form.getlist('weights[]')
		units = request.form.getlist('values[]')

		image = ''
		if 'image' in request.files:
			file = request.files['image']
			if file:

				### claudira

				# upload_result = upload(file)
				# thumbnail_pixelate, options = cloudinary_url(
				# upload_result['public_id'],
				# format="jpg",
				# crop="fill",
				# width=350,
				# height=234,
				# radius=0,
				# gravity="center"
				# )
				# image = thumbnail_pixelate


				### manul
				filename = file.filename
				path = "public/uploads/"+name.replace(" ","_").replace("#","_").replace(".","_")+"."+filename.split(".")[-1]
				image = "/uploads/"+name.replace(" ","_").replace("#","_").replace(".","_")+"."+filename.split(".")[-1]
				file.save(path)

		obj = RecipeModel(name=name , tag_id=tag_id  , direction=direction  , image=image , ingredients=ingredients , amounts=amounts , units=units )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/recipe/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/recipe/create.html')
	return "404"



@recipe_blueprint.route("admin/recipe/validator/uniquename" , methods =['GET',"POST"])
@flask_login.login_required
def unique_name_validator():

	from db_models import RecipeModel


	response = {'valid':'true'}
	name = request.args.get('name')
	print(name)

	# item = RecipeModel.query.filter_by(name=name).first()
	item = RecipeModel.query.filter(func.lower(RecipeModel.name) == func.lower(name)).first()

	if item:
		response['valid'] = 'false'


	return jsonify(response)


