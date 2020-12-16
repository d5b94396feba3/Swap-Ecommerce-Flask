from flask import render_template,request, redirect,url_for,flash,session,current_app
from src import app, db
from src.products.models import Addproduct
from src.products.routes import apparels,categories


def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart',methods=['POST'])
def AddCart():
	try:
		product_id=request.form.get('product_id')
		quantity=request.form.get('quantity')
		sizes=request.form.get('sizes')
		product=Addproduct.query.filter_by(id=product_id).first()

		if product_id and quantity and sizes and request.method=="POST":
			DictItems={product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,
			'size':sizes,'quantity':int(quantity),'image':product.image_1,'sizes':product.sizes,'stock':product.stock}}

			if 'cart' in session:
				print(session['cart'])
				if product_id in session['cart']:
					for key, item in session['cart'].items():
						if int(key) == int(product_id):
							session.modified=True
							item['quantity']+=1
				else:
					session['cart'] = MagerDicts(session['cart'], DictItems)
					return redirect(request.referrer)
			else:
				session['cart']=DictItems
				return redirect(request.referrer)
	except Exception as e:
		print(e)
	finally:
		return redirect(request.referrer)


@app.route('/carts')
def getCart():
	if 'cart' not in session or len(session['cart']) <= 0:
		return redirect(url_for('index'))

	subtotal=0
	grandtotal=0
	for key,product in session['cart'].items():
		discount=(product['discount']/100) * float(product['price'])
		subtotal+=float(product['price']*int(product['quantity']))
		subtotal-=discount
	tax=("%.2f" % (.06 * float(subtotal)))
	grandtotal=float("%.2f" % (1.06 * subtotal))
	return render_template('products/carts.html',tax=tax,grandtotal=grandtotal,
		apparels=apparels(),categories=categories())




@app.route('/updatecart/<int:code>',methods=['POST'])
def updatecart(code):
	if 'cart' not in session or len(session['cart']) <= 0:
		return redirect(url_for('index'))
	if request.method=="POST":
		quantity=request.form.get('quantity')
		size=request.form.get('size')
		try:
			session.modified=True
			for key, item in session['cart'].items():
				if int(key) == code:
					item['quantity']=quantity
					item['size']=size
					flash('Your cart has been updated!','success')
					return redirect(url_for('getCart'))

		except Exception as e:
			print(e)
			return redirect(url_for('getCart'))


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
	if 'cart' not in session or len(session['cart']) <= 0:
		return redirect(url_for('index'))
	
	try:
		session.modified=True
		for key, item in session['cart'].items():
			if int(key) == id:
				session['cart'].pop(key,None)

				#flash('Item has been deleted!','success')
				return redirect(url_for('getCart')) 

	except Exception as e:
		print(e)
		return redirect(url_for('getCart'))




@app.route('/clearcart')
def clearcart():
	try:
		session.pop('cart',None)
		return redirect(url_for('index'))
	except Exception as e:
		print(e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404
