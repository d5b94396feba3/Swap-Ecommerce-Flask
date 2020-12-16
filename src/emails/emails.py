from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import render_template,request,redirect,url_for,flash,session
from src import app,db,mail,urlSTS
from flask_login import login_required, current_user
from flask_mail import Message
import secrets


def recipient_email():
    return current_user.email


def default_email():
    return 'windowsking55@gmail.com' #mail username


@app.route('/account/confirmation/sent')
def confirm_account():

    recipient=recipient_email()
    sender=default_email()
    token = urlSTS.dumps(recipient, salt='email-confirm')
    msg = Message('Confirm Your Account', sender=sender, recipients=[recipient])
    link = url_for('confirm_email', token=token, _external=True)
    msg.html=render_template('email/layout.html', user=current_user,url=link)
    mail.send(msg)
    # send_async_email(app, msg)
    session['email']=True
    return redirect(url_for('customer_profile'))



@app.route('/confirm/<token>', methods=["GET", "POST"])
def confirm_email(token):
    try:
        email = urlSTS.loads(token, salt="email-confirm", max_age=86400)
    except:
        abort(404)
    flash('You have confirmed your account. Thanks!', 'success')
    user=current_user
    user.is_confirm=True
    db.session.commit()
    return redirect(url_for('customer_profile'))
 


def purchase_confirmation():

    recipient=recipient_email()
    sender=default_email()
    token = urlSTS.dumps(recipient, salt='purchase-confirm')
    msg = Message('Payment Successfull.', sender=sender, recipients=[recipient])
    msg.html=render_template('email/purchase.html', user=current_user)
    mail.send(msg)


def send_password(password,email):

    recipient=email
    sender=default_email()
    token = urlSTS.dumps(recipient, salt='password-confirm')
    msg = Message('Reset Password', sender=sender, recipients=[recipient])
    msg.html=render_template('email/change_password.html', user=current_user,password=password)
    mail.send(msg)
    print('send_password')
    flash(f'Password sent to your email.', 'success')
    return redirect(url_for('login'))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404