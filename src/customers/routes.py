from flask import render_template,request, redirect,url_for,flash,session
from src import app,db,photos,bcrypt,login_manager,mail,urlSTS
from flask_login import login_required, current_user, logout_user, login_user
import secrets
from .forms import CustomerRegisterForm,LoginForm,CustomerUpdateForm,ChangePasswordForm
from .models import Register,CustomerOrder,OrderHistory
from ..products.routes import apparels,categories 
from src.admin.models import User
from is_safe_url import is_safe_url



@app.route('/dashboard/profile')
@login_required
def customer_profile():
    
    customer_orders=OrderHistory.query.filter_by(customer_id=current_user.id).order_by(OrderHistory.id.desc()).all()
    print(customer_orders)
    return render_template('customer/profile.html',customer_orders=customer_orders,
        user=current_user,apparels=apparels(),categories=categories())


@app.route('/dashboard/update/profile',methods=['GET','POST'])
@login_required
def update_customer_profile():


    form=CustomerUpdateForm()

    user = Register.query.filter_by(id=current_user.id).first()

    update_email=form.email.data
    update_confirm_password=request.form.get('ct_update_confirm_password')
    update_name=form.name.data

    if request.method=="POST":

        if update_name:
            user.name=update_name
            flash(f"Your Name have been updated","success")
            db.session.commit()
            return redirect(url_for('update_customer_profile'))

        elif update_email:
            email_exist=Register.query.filter_by(email=update_email).first()

            if email_exist:
                flash(f"Email already exist.","danger")
            else:          
                user.email=update_email
                user.is_confirm=False
                flash(f"Your Email have been updated","success")
                db.session.commit()

            return redirect(url_for('update_customer_profile'))

        elif update_confirm_password:
            user.password=bcrypt.generate_password_hash(update_confirm_password)
            flash(f"Your Password have been updated","success")
            db.session.commit()
            return redirect(url_for('update_customer_profile'))

        else:
            user.city=form.city.data
            user.zipcode=form.zipcode.data
            user.contact=form.contact.data
            user.address=form.address.data
            user.country=form.country.data
            print('Your Address have been updated')
            flash(f"Your Address have been updated","success")
            db.session.commit()
            return redirect(url_for('update_customer_profile'))

    form.name.data=user.name
    form.email.data=user.email
    form.city.data=user.city
    form.zipcode.data=user.zipcode
    form.contact.data=user.contact
    form.address.data=user.address
    form.country.data=user.country

    return render_template('customer/update_profile.html',user=current_user,
        form=form,apparels=apparels(),categories=categories())



@app.route('/register',methods=['GET','POST'])
def customer_register():
    form=CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
            password=hash_password,country=form.country.data, city=form.city.data,
            contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Thank you for signing up with us!', 'success')
        db.session.commit()
        session['email']=False
        return redirect(url_for('login'))
    return render_template('customer/register.html',form=form,apparels=apparels(),
            categories=categories())




@app.route('/change/password',methods=['GET','POST'])
def change_password():
    form=ChangePasswordForm()

    if form.validate_on_submit():
        email=form.email.data
        password=secrets.token_hex(6)
        print('email: ',email)
        print('password: ',password)

        user=Register.query.filter_by(email=email).first()

        if user:
            user.password=bcrypt.generate_password_hash(password)
            db.session.commit()
            send_password(password,email)
        else:          
            flash(f"Sorry, no user account found.","danger")


    return render_template('change_password.html',form=form,apparels=apparels(),
            categories=categories())




@app.route('/login',methods=['GET','POST'])
def login():


    form=LoginForm()

    if form.validate_on_submit():
        # user login
        user=Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            session['is_admin']=False
            if not user.is_confirm:
                session['email']=False
            # next=request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            return redirect(url_for('index'))


        # admin login
        user=User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data): 
            login_user(user)
            session['is_admin']=True
            session['name']=current_user.name
            session['image']=current_user.profile
            # next=request.args.get('next')
            return redirect(url_for('dashboard'))


        flash('Incorrect email and password','danger')
        return redirect(url_for('login'))

    return render_template('login.html',form=form,apparels=apparels(),
            categories=categories())


@app.route('/logout')
def logout():
    logout_user()
    session.pop('is_admin',None)
    session.pop('email',None)
    session.pop('name',None)
    session.pop('image',None)
    return redirect(url_for('index'))


#add_category instead of category
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user,apparels=apparels(),
            categories=categories()), 404