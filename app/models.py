from datetime import datetime

from sqlalchemy_utils.types.choice import ChoiceType

from app import db


#from sqlalchemy import Column, String, Integer

class BaseModel(db.Model):
    __abstract__ = True

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)

    def __repr__(self):
        repr_fields = getattr(self, '__repr_fields__', ['id'])

        repr_values = ', '.join(
            '{}:{}'.format(
                repr_field,
                getattr(self, repr_field, None)
            )
            for repr_field in repr_fields
        )

        return "<class:{} {}>".format(
            self.__class__.__name__,
            repr_values
        )

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.query.filter(*args, **kwargs)

    @classmethod
    def get(cls, id: int):
        return cls.query.get(id)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()
#
class Customer(BaseModel):
    __tablename__ = 'customer'
    __repr_fields__ = ['id', 'name', 'orgnr', 'trunks']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    orgnr = db.Column(db.String())
    trunks = db.relationship('Trunk', secondary=lambda: customer_trunk_association)
    features = db.relationship('Feature', secondary=lambda: customer_feature_association) #lambda so association table config can be below classes due to read order
    contacts = db.relationship('Contact', back_populates='customers')
    deliveries = db.relationship('Delivery', back_populates='customer')
    ppi = db.Column(db.String())

#
class Trunk(BaseModel):
    '''Write 'trunks.update()' to update trunks according to list'''
    __tablename__= 'trunk'
    __repr_fields__ = ['id', 'trunk']
    id = db.Column(db.Integer(), primary_key=True)
    trunk = db.Column(db.String())
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'))
    carrier = db.relationship('Carrier', back_populates='trunks')
    customers = db.relationship('Customer', secondary=lambda: customer_trunk_association, back_populates='trunks')
#
class Carrier(BaseModel):
    '''List of carriers'''
    __tablename__= 'carrier'
    __repr_fields__ = ['id', 'name']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    trunks = db.relationship('Trunk', back_populates='carrier')
    downtimes = db.relationship('Downtime', back_populates='carrier')
#
class Feature(BaseModel):
    '''Keeps customer features in sync'''
    __tablename__ = 'feature'
    __repr_fields__ = ['id', 'feature_id', 'feature_name']
    id = db.Column(db.Integer(), primary_key=True)
    feature_id = db.Column(db.String())
    feature_name = db.Column(db.String())
    customers = db.relationship('Customer', secondary=lambda: customer_feature_association,
                                back_populates='features')
#
class Downtime(BaseModel):
    '''Registrered Downtimes'''
    __tablename__ = 'downtime'
    __repr_fields__ = ['id', 'carrier_name', 'downfrom', 'downto']
    id = db.Column(db.Integer(), primary_key=True)
    downfrom = db.Column(db.DateTime())
    downto = db.Column(db.DateTime())
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'))
    carrier = db.relationship('Carrier', back_populates='downtimes')

    @property
    def carrier_name(self):
        '''Get carrier name for Downtime'''
        return self.carrier.name

#
class Contact(BaseModel):
    '''Contacts'''
    __tablename__ = 'contact'
    __repr_fields__ = ['id', 'name', 'phone', 'email', 'customer']
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    comments = db.Column(db.String())
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customers = db.relationship('Customer', back_populates='contacts')

    @property
    def name(self):
        '''Merges firstname and last name into 'name'''
        return self.firstname + " " + self.lastname

#
class Delivery(BaseModel):
    '''Delivery'''
    __tablename__ = 'delivery'
    __repr_fields__ = ['id', 'date', 'done_date', 'live_date', 'customer', 'internal_comments']
    id = db.Column(db.Integer(), primary_key=True)
    order_date = db.Column(db.DateTime())
    completed_date = db.Column(db.DateTime())
    live_date = db.Column(db.DateTime())
    customer = db.relationship('Customer', back_populates='deliveries')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    #user
    comments = db.Column(db.String())
    internal_comments =  db.Column(db.String())
    work_items = db.relationship('DeliveryWorkItem', back_populates='delivery')
#
class DeliveryWorkItem(BaseModel):
    '''Delivery work items'''
    __tablename__ = 'delivery_work_item'
    __repr_fields__ = ['id', 'name', 'text', 'completed', 'date', 'due_date']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    text = db.Column(db.String())
    due_date = db.Column(db.DateTime())
    completed = db.Column(db.Boolean, default=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'))
    delivery = db.relationship('Delivery', back_populates='work_items')
#
class User(BaseModel):
    '''User'''
    __tablename__ = 'user'
    __repr_fields__ = ['id', 'name', 'access_level']
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    name = db.Column(db.String())
    email = db.Column(db.String())
    access_level = db.Column(db.String()) #(admin(0), regular(1), read_only(2))
    password_hash = db.Column(db.String())
    ews_url = db.Column(db.String())
#
class WikiArticle(BaseModel):
    '''Wiki'''
    __tablename__ = 'wiki_article'
    __repr_fields__ = ['id', 'heading', 'text']
    id = db.Column(db.Integer(), primary_key=True)
    heading = db.Column(db.String())
    text = db.Column(db.String())
    category = db.relationship('WikiCategory', secondary=lambda: wiki_category_association, backref='wikipost')
    tags = db.relationship('Tag', secondary=lambda: wiki_tag_association, backref='wikipost')

#
class WikiCategory(BaseModel):
    '''Wiki Category'''
    __tablename__ = 'wiki_category'
    __repr_fields__ = ['id', 'name']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

#
class Tag(BaseModel):
    '''General tags'''
    __tablename__ = 'tag'
    __repr_fields__ = ['id', 'name']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
#
class Todo(BaseModel):
    '''Todo'''
    __tablename__ = 'todo'
    __repr_fields__ = ['id', 'name', 'text', 'completed', 'date', 'due_date']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    text = db.Column(db.String()) #optional
    due_date = db.Column(db.DateTime()) #optional
    completed = db.Column(db.Boolean, default=False)
    speedy = db.Column(db.Boolean, default=True)

#
class Inventory(BaseModel):
    '''Inventory'''
    __tablename__ = 'inventory'
    __repr_fields__ = ['id', 'brand', 'item', 'text', 'condition', 'price', 'stock']
    id = db.Column(db.Integer(), primary_key=True)
    brand = db.Column(db.String())
    item = db.Column(db.String())
    text = db.Column(db.String())
    price = db.Column(db.Integer())
    stock = db.Column(db.Integer())

    CONDITION = (
        ('new', 'ny'),
        ('used', 'brukt'))
    condition = db.Column(ChoiceType(CONDITION), default='new')
#
class Porting(BaseModel):
    '''Porting'''
    __tablename__ = 'porting'
    __repr_fields__ = ['id', 'number', 'porting_date', 'status']
    id = db.Column(db.Integer(), primary_key=True)
    customer = db.Column(db.String())
    orgnr = db.Column(db.String())
    number_series = db.Column(db.String())
    porting_date = db.Column(db.DateTime())
    status = db.Column(db.String())

#
class UserCalendarItem(BaseModel):
    '''User calendar'''
    __tablename__ = 'user_calendar'
    __repr_fields__ = ['id', 'user', 'heading', 'body', 'date']
    id = db.Column(db.Integer(), primary_key=True)
    heading = db.Column(db.String())
    body = db.Column(db.String())
    date = db.Column(db.DateTime())
    user = db.relationship('User', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
class WavePriceList(BaseModel):
    '''Price for Wave features'''
    __tablename__ = 'wave_price_list'
    __repr_fields__ = ['id', 'name', 'price']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
#

wiki_category_association = db.Table('wiki_category_association',
    db.Column('wiki_id', db.Integer, db.ForeignKey('wiki_article.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('wiki_category.id'))
    )

wiki_tag_association = db.Table('wiki_tag_association',
    db.Column('wiki_id', db.Integer, db.ForeignKey('wiki_article.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    )

customer_trunk_association = db.Table('customer_trunk_association',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('trunk_id', db.Integer, db.ForeignKey('trunk.id'))
    )

customer_feature_association = db.Table('customer_feature_association',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'))
    )


#leveranse
#todo
#wiki/notes

'''
back end -> Flask/SQL Alchemy

routing -> Flask

front end -> Jinja2? React.js?

platforms{
    tdc{
      customerid{
            Name
            trunks
            Features
        }
    }
    hafslund{
        customerid{
            Name
            trunks
            Features
        } 
    }
}


Record sound messages

Record open and 

'''
