from src import db,login_manager
from datetime import datetime
from flask_login import UserMixin
import json



@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_confirm=db.Column(db.Boolean, nullable=False,default=False)


    def __repr__(self):
        return '<Register %r>' % self.name



class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice



class OrderHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=False,nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    customer_name = db.Column(db.String(50), unique= False)
    country = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    product_id = db.Column(db.Integer, unique=False, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_price=db.Column(db.Numeric(10,2),nullable=False)
    product_quantity=db.Column(db.Integer,nullable=False)
    product_detail = db.Column(db.String(80),default='None',nullable=False)
    product_brand = db.Column(db.String(50),default='None', unique= False)
    product_category = db.Column(db.String(50),default='None', unique= False)
    payment_method = db.Column(db.String(50),default='Stripe', unique= False)
    product_delivered= db.Column(db.String(20),default='False', unique= False)
    delivered_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    product_image=db.Column(db.String(150),nullable=False,default='product_image.jpg')
    product_cancel= db.Column(db.Boolean, nullable=False,default=False)





    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


db.create_all()