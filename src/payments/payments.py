from flask import render_template,request, redirect,url_for,flash,session,make_response
from src import app,db,bcrypt,login_manager,mail,urlSTS
from flask_login import login_required, current_user, login_user
import secrets
from src.customers.models import Register,CustomerOrder,OrderHistory
from ..products.routes import apparels,categories 
from src.admin.models import User
from src.emails.emails import purchase_confirmation,send_password
import os
import pdfkit
import stripe




publishable_key='' # your publishable_key

stripe.api_key=''  # your stripe api key


@app.route('/payment/confirm',methods=['POST'])
@login_required
def payment(): 

    invoice=request.form.get('invoice')
    amount=request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
      customer=customer.id,
      description='Swap Online Shopping',
      amount=amount,
      currency='usd',
    )
    orders=CustomerOrder.query.filter_by(customer_id=current_user.id, 
        invoice=invoice).order_by(CustomerOrder.id.desc()).first()

    current_id=current_user.id
    customer=Register.query.filter_by(id=current_id).first()

    orders=CustomerOrder.query.filter_by(customer_id=current_id, 
        invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    
    for _key, product in orders.orders.items():

        order=OrderHistory(invoice=invoice,status="Paid", customer_id=current_id,
            customer_name=customer.name,country=customer.country,city=customer.city,
            contact=customer.contact,zipcode=customer.zipcode,
            product_id=int(_key),product_name=product['name'],
            product_price=product['price'],product_quantity=product['quantity'],
            product_detail=product['size'],product_image=product['image'])

        db.session.add(order)
        print('Your order has been sent successfully','success')
    

    orders.status="Paid"
    db.session.commit()
    purchase_confirmation()
    return redirect(url_for('thanks'))




@app.route('/get/order')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id=current_user.id
        invoice=secrets.token_hex(5)

        try:
            order=CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['cart'])
            db.session.add(order)
            db.session.commit()
            session.pop('cart')
            return redirect(url_for('orders',invoice=invoice))

        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order','danger')
            return redirect(url_for('getCart'))



@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal=0
        subTotal=0
        customer_id=current_user.id
        customer=Register.query.filter_by(id=customer_id).first()
        orders=CustomerOrder.query.filter_by(customer_id=customer_id, 
            invoice=invoice).order_by(CustomerOrder.id.desc()).first()


        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
        tax = ("%.2f" % (.06 * float(subTotal)))
        grandTotal = ("%.2f" % (1.06 * float(subTotal)))
    else:
        return redirect(url_for('login'))
    return render_template('customer/order.html', invoice=invoice, tax=tax,
        subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders,apparels=apparels(),categories=categories())



@app.route('/orders/get_pdf/<invoice>',methods=['POST'])
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal=0
        subTotal=0
        customer_id=current_user.id

        if request.method=="POST":
            customer=Register.query.filter_by(id=customer_id).first()
            orders=CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax,
                grandTotal=grandTotal,customer=customer,orders=orders)

            
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            #pdf=pdfkit.from_url(rendered, 'out-test.pdf', configuration=config)
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response=make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline: filename='+invoice+'.pdf'
            return response
    return redirect(url_for('orders'))




@app.route('/order/cancel/<int:id>')
@login_required
def order_cancel(id):
    order=OrderHistory.query.get_or_404(id)
    order.product_cancel=True
    db.session.commit()
    flash('Order Canceled!')
    return redirect(url_for('customer_profile'))


@app.route('/thanks')
@login_required
def thanks():
    return render_template('customer/thank.html',apparels=apparels(),categories=categories())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404