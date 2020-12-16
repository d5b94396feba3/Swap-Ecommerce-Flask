from src import db


from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Numeric(10,2),nullable=False)
    discount=db.Column(db.Integer,default=0)
    stock=db.Column(db.Integer,nullable=False)
    colors=db.Column(db.Text,nullable=False,default='none')
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    apparel_id = db.Column(db.Integer, db.ForeignKey('apparel.id'),
        nullable=False)
    apparel = db.relationship('Apparel',
        backref=db.backref('apparels', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('categories', lazy=True))

    image_1=db.Column(db.String(150),nullable=False,default='image.jpg')
    image_2=db.Column(db.String(150),nullable=False,default='image.jpg')
    image_3=db.Column(db.String(150),nullable=False,default='image.jpg')

    sizes=db.Column(db.Text,nullable=False,default='none')



    def __repr__(self):
        return '<Addproduct %r>' % self.name


class Apparel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False,unique=True)

class Category(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(30),nullable=False,unique=True)

db.create_all()