from flask import render_template, session, request, redirect,url_for,flash,current_app
from datetime import datetime
from src import app,db,bcrypt,photos
from .forms import RegistrationForm
from flask_login import login_required, current_user, logout_user, login_user
from .models import User
from src.products.models import Addproduct,Apparel,Category
from src.customers.models import Register,CustomerOrder,OrderHistory 
import secrets
import os


def is_admin():
    id=current_user.id
    user=User.query.get_or_404(id)
    return user.is_admin

@app.route('/dashboard/admin')
@login_required
def dashboard():
    if is_admin():
        products=Addproduct.query.all()
        return render_template('admin/dashboard.html',products=products)


@app.route('/dashboard/orders')
@login_required
def dashboard_orders():

    if is_admin():
        orders=OrderHistory.query.all()
        return render_template('admin/orders.html',orders=orders)



@app.route('/dashboard/update/orders/<int:id>',methods=['GET','POST'])
@login_required
def update_orders(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    orders=OrderHistory.query.get_or_404(id)
    if request.method=="POST":
        orders.product_delivered='True'
        orders.delivered_time=datetime.utcnow()
        print(f'The product {orders.product_name} has been updated','success')
        db.session.commit()
        return redirect(url_for('dashboard_orders'))

    return render_template('admin/update_orders.html',orders=orders)


@app.route('/dashboard/unconfirm/orders/<int:id>',methods=['GET','POST'])
@login_required
def unconfirm_orders(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    orders=OrderHistory.query.get_or_404(id)
    if request.method=="POST":
        orders.product_delivered='False'
        orders.delivered_time=datetime.utcnow()
        print(f'The product {orders.product_name} has been updated','success')
        db.session.commit()
        return redirect(url_for('dashboard_orders'))

    return render_template('admin/update_orders.html',orders=orders)


@app.route('/dashboard/edit',methods=['GET','POST'])
@login_required
def update_admin_profile():
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    user = User.query.filter_by(id=current_user.id).first()

    print('user',user)
    if request.method=="POST":
        update_name=request.form.get('update_name')
        if update_name is not None:
            user.name=update_name
            flash(f"Your Name have been updated","success")
            db.session.commit()
            return redirect(url_for('update_admin_profile'))

        update_email=request.form.get('update_email')
        if update_email is not None:
            user.email=update_email
            flash(f"Your Email have been updated","success")
            db.session.commit()
            return redirect(url_for('update_admin_profile'))

        update_confirm_password=request.form.get('update_confirm_password')
        if update_confirm_password is not None:
            user.password=bcrypt.generate_password_hash(update_confirm_password)
            flash(f"Your Password have been updated","success")
            db.session.commit()
            return redirect(url_for('update_admin_profile'))


        update_photo=request.files.get('update_photo')
        if update_photo:
            print(update_photo)
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + user.profile))
                user.profile = photos.save(update_photo, name=secrets.token_hex(10) + ".")
            except:
                user.profile = photos.save(update_photo, name=secrets.token_hex(10) + ".")
    
            flash(f"Your Profile image been updated","success")
            db.session.commit()
            return redirect(url_for('update_admin_profile'))


    return render_template('admin/update_profile.html')




@app.route('/dashboard/user/<string:name>')
@login_required
def dashboard_users(name=''):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    customers=Register.query.all()
    admins=User.query.all()
    if name == 'admin':
        return render_template('admin/users.html',admins=admins)  
    else:
        return render_template('admin/users.html',customers=customers)


@app.route('/dashboard/products')
@login_required
def products():
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    page=request.args.get('page',1,type=int)
    products=Addproduct.query.filter(Addproduct.stock>0).order_by(Addproduct.id.desc()).paginate(page=page,per_page=8)

    return render_template('admin/products.html',products=products)



@app.route('/apparels')
@login_required
def apparels():
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    apparels=Apparel.query.order_by(Apparel.id.desc()).all()  
    return render_template('admin/products.html',apparels=apparels) 



@app.route('/categories')
@login_required
def categories():
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    categories=Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/products.html',categories=categories)


@app.route('/administrator/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            hash_password=bcrypt.generate_password_hash(form.password.data)
            user=User(name=form.name.data,username=form.username.data,email=form.email.data,
                password=hash_password,access=form.access.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {form.name.data} Thank you for registering','success')
            return redirect(url_for('dashboard'))
        else:
            print(form.errors)
    except Exception as e:
        print(e)
    return render_template('admin/register.html', form=form)


@app.route('/dashboard/user/<int:id>',methods=['GET','POST'])
@login_required
def delete_admin_user(id):
    if is_admin() is False:
        return register_error_handler(404, page_not_found)

    user=User.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(user)
        flash(f'The user {user.name} was deleted from your database','success')
        db.session.commit()
        return redirect(url_for('dashboard_users',name='admin'))
    flash(f'The user {user.name} cant be deleted','warning')
    return render_template(url_for('dashboard'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404
