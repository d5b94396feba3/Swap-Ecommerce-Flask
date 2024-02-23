from flask import render_template,request, redirect,url_for,flash,session,current_app

from src import app,db,photos
import secrets
from flask_login import login_required
from .models import Category,Addproduct,Apparel,Sliders
from .forms import Addproducts
from src.admin.routes import is_admin
from flask_login import login_required, current_user, logout_user, login_user
from src.admin.models import User
import os

def apparels():
	apparels=Apparel.query.join(Addproduct,(Apparel.id==Addproduct.apparel_id)).all()
	return apparels

def categories():
	categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
	return categories

def sliders():
	slider_images=Sliders.query.all()
	print('slider_images: ',slider_images)
	return slider_images

def remove_slider_images():
	db.session.query(Sliders).delete()
	db.session.commit()

@app.route('/')
def index():
	page=request.args.get('page',1,type=int)
	products=Addproduct.query.filter(Addproduct.stock>0).order_by(Addproduct.id.desc()).paginate(page=page,per_page=8)
	return render_template('products/index.html',products=products,apparels=apparels(),
		categories=categories(),sliders=sliders())

@app.route('/product/search',methods=['GET','POST'])
def search():

	page=request.args.get('page',1,type=int)
	keyword=request.form.get('search')
	if keyword == '':
		return render_template('products/search.html',apparels=apparels(),
			categories=categories())
	elif keyword is not None:
		search = "%{}%".format(keyword)
		keywords=Addproduct.query.filter(Addproduct.name.like(search)).all()
		return render_template('products/search.html',apparels=apparels(),
			categories=categories(),keywords=keywords,keyword=keyword)
	else:
		return render_template('products/search.html',apparels=apparels(),
			categories=categories(),keywords=keyword)

@app.route('/product/id/<int:id>')
def product_detail(id):
	product=Addproduct.query.get_or_404(id)
	product_id=id
	print('product_id:',product_id)
	print('product-name:',product.name)
	category=Category.query.filter_by(id=product.category_id).first_or_404()
	print('category',category)
	products=Addproduct.query.filter_by(category=category).limit(4).all()
	print('products:',products)
	return render_template('products/product_detail.html',product=product,apparels=apparels(),
		categories=categories(),products=products,product_id=product_id)	



@app.route('/apparel/id/<int:id>')
def get_apparels(id):
	page=request.args.get('page',1,type=int)
	apparel_pages=Apparel.query.filter_by(id=id).first_or_404()
	apparel=Addproduct.query.filter_by(apparel=apparel_pages).paginate(page=page,per_page=8)
	return render_template('products/index.html',apparel=apparel,apparels=apparels(),
		categories=categories(),apparel_pages=apparel_pages,sliders=sliders())

@app.route('/category/id/<int:id>')
def get_categories(id):
	page=request.args.get('page',1,type=int)
	category=Category.query.filter_by(id=id).first_or_404()
	category_pages=Addproduct.query.filter_by(category=category).paginate(page=page,per_page=8)
	return render_template('products/index.html',category_pages=category_pages,
		categories=categories(),apparels=apparels(),category=category,sliders=sliders())


@app.route('/upload/slide/images',methods=['GET','POST'])
@login_required
def upload_slide_images():
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)


		# image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
		# image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
		# image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")

	# user = User.query.filter_by(id=current_user.id).first()
	# slider_images=sliders()
	if request.method == "POST":
		remove_slider_images()
		# Sliders
		update_photo1=request.files.get('slide_image_1')
		update_photo2=request.files.get('slide_image_2')
		update_photo3=request.files.get('slide_image_3')
		image_1 = photos.save(update_photo1,name=secrets.token_hex(10) + ".")
		image_2 = photos.save(update_photo2,name=secrets.token_hex(10) + ".")
		image_3 = photos.save(update_photo3,name=secrets.token_hex(10) + ".")
		# if update_photo:
		#     print('upload img-1:',update_photo)
		#     try:
		#         os.unlink(os.path.join(current_app.root_path, "static/images/" + Sliders.slide_image_1))
		#         Sliders.slide_image_1 = photos.save(update_photo, name=secrets.token_hex(10) + ".")
		#     except:
		#         Sliders.slide_image_1 = photos.save(update_photo, name=secrets.token_hex(10) + ".")

		#     # flash(f"Home Slide image 1 has been updated","success")
		#     # db.session.commit()
		#     # return redirect(url_for('upload_slide_images'))

		# update_photo=request.files.get('slide_image_2')
		# if update_photo:
		#     print('upload img-2:',update_photo)
		#     try:
		#         os.unlink(os.path.join(current_app.root_path, "static/images/" + Sliders.slide_image_2))
		#         Sliders.slide_image_2 = photos.save(update_photo, name=secrets.token_hex(10) + ".")
		#     except:
		#         Sliders.slide_image_2 = photos.save(update_photo, name=secrets.token_hex(10) + ".")

		#     # flash(f"Home Slide image 2 has been updated","success")
		#     # db.session.commit()
		#     # return redirect(url_for('upload_slide_images'))

		# update_photo=request.files.get('slide_image_3')
		# if update_photo:
		#     print('upload img-3:',update_photo)
		#     try:
		#         os.unlink(os.path.join(current_app.root_path, "static/images/" + Sliders.slide_image_3))
		#         Sliders.slide_image_3 = photos.save(update_photo, name=secrets.token_hex(10) + ".")
		#     except:
		#         Sliders.slide_image_3 = photos.save(update_photo, name=secrets.token_hex(10) + ".")
		add_slide_images = Sliders(slide_image_1=image_1,slide_image_2=image_2,
			slide_image_3=image_3)

		flash(f"Home Slide images have been updated","success")
		db.session.add(add_slide_images)
		db.session.commit()
		return redirect(url_for('upload_slide_images'))



	return render_template('products/upload_slide_images.html')


@app.route('/add/category',methods=['GET','POST'])
@login_required
def add_category():
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)

	if request.method == "POST":
		getcat=request.form.get('category')
		cat=Category(name=getcat)
		db.session.add(cat)
		flash(f'The category {getcat} was added successfully.','success')
		db.session.commit()
		return redirect(url_for('categories'))
	return render_template('products/add_apparel.html')


@app.route('/update/apparel/<int:id>',methods=['GET','POST'])
@login_required
def update_apparel(id):
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)
	update_apparel=Apparel.query.get_or_404(id)
	apparel=request.form.get('apparel_update')
	if request.method=="POST":
		update_apparel.name=apparel
		flash(f'The apparel {update_apparel.name} was updated successfully.','success')
		db.session.commit()
		return redirect(url_for('apparels'))
	return render_template('products/update_apparel.html',title='Update Apparel Page',
		update_apparel=update_apparel)



@app.route('/delete/apparel/<int:id>',methods=['GET','POST'])
@login_required
def delete_apparel(id):
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)
	apparel=Apparel.query.get_or_404(id)
	if request.method=="POST":
		db.session.delete(apparel)
		flash(f'The apparel {apparel.name} was deleted successfully.','success')
		db.session.commit()
		return redirect(url_for('apparels'))

	flash(f'The apparel {apparel.name} cant be deleted','warning')
	return render_template(url_for('products'))




@app.route('/delete/category/<int:id>',methods=['GET','POST'])
@login_required
def delete_category(id):
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)
	category=Category.query.get_or_404(id)
	if request.method=="POST":
		db.session.delete(category)
		flash(f'The category {category.name} was deleted successfully.','success')
		db.session.commit()
		return redirect(url_for('category'))

	flash(f'The category {category.name} cant be deleted','warning')
	return render_template(url_for('products'))



@app.route('/update/category/<int:id>',methods=['GET','POST'])
@login_required
def update_category(id):
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)
	update_category=Category.query.get_or_404(id)
	category=request.form.get('category_update')
	if request.method=="POST":
		update_category.name=category
		flash(f'The Category {update_category.name} was updated successfully.','success')
		db.session.commit()
		return redirect(url_for('category'))
	return render_template('products/update_apparel.html',title='Update category Page',
		update_category=update_category)



@app.route('/add/apparel',methods=['GET','POST'])
@login_required
def add_apparel():
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)

	if request.method == "POST":
		getapparel=request.form.get('apparel')
		apparel=Apparel(name=getapparel)
		db.session.add(apparel)
		flash(f'The Apparel {getapparel} was added successfully.','success')
		db.session.commit()
		return redirect(url_for('apparels'))
	return render_template('products/add_apparel.html', apparels='apparels')



@app.route('/add/product',methods=['POST','GET'])
@login_required
def add_product():
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)

	apparels=Apparel.query.all()

	categories=Category.query.all()
	form=Addproducts(request.form)
	if request.method=="POST":

		name = form.name.data
		price = form.price.data
		discount = form.discount.data
		stock = form.stock.data
		sizes = form.sizes.data
		desc = form.discription.data
		apparel = request.form.get('apparel')

		category = request.form.get('category')		
		image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
		image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
		image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")


		addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,
			sizes=sizes,desc=desc,category_id=category,apparel_id=apparel,
			image_1=image_1,image_2=image_2,image_3=image_3)

		db.session.add(addproduct)

		flash(f'The product {name} was added successfully.','success')

		db.session.commit()

		return redirect(url_for('products'))

	return render_template('products/add_product.html', title='Add products page',form=form,
		apparels=apparels,categories=categories)


@app.route('/update/product/id/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):
	
	if is_admin() is False:
	    return register_error_handler(404, page_not_found)

	apparels=Apparel.query.all()

	categories=Category.query.all()
	product=Addproduct.query.get_or_404(id)
	apparel=request.form.get('apparel')

	category=request.form.get('category')
	form = Addproducts(request.form)

	if request.method =="POST":
	    product.name = form.name.data 
	    product.price = form.price.data
	    product.discount = form.discount.data
	    product.stock = form.stock.data 
	    product.sizes = form.sizes.data
	    product.desc = form.discription.data
	    product.category_id = category
	    product.apparel_id = apparel 

	    if request.files.get('image_1'):
	        try:
	            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
	            print(product.image_1)
	            product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
	        except:
	            product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
	    if request.files.get('image_2'):
	        try:
	            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
	            product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
	        except:
	            product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
	    if request.files.get('image_3'):
	        try:
	            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
	            product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
	        except:
	            product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

	    flash('The product was updated','success')
	    db.session.commit()
	    return redirect(url_for('products'))

	form.name.data=product.name
	form.price.data=product.price
	form.discount.data=product.discount
	form.stock.data=product.stock
	form.sizes.data=product.sizes
	form.discription.data=product.desc
	return render_template('products/update_product.html',form=form,title="Update Product",
	    apparels=apparels,categories=categories,product=product)



@app.route('/delete/product/<int:id>',methods=['GET','POST'])
@login_required
def delete_product(id):

	if is_admin() is False:
	    return register_error_handler(404, page_not_found)

	product = Addproduct.query.get_or_404(id)

	if request.method =="POST":
		try:
		    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
		    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
		    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
		except Exception as e:
		    print(e)

		db.session.delete(product)
		flash(f'The product {product.name} was deleted successfully.','success')
		db.session.commit()
		return redirect(url_for('products'))

	flash(f'The product {product.name} cant be deleted','warning')
	return render_template(url_for('products'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user,apparels=apparels(),
			categories=categories()), 404