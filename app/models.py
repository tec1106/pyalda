from datetime import datetime
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

class Customer(BaseModel):
    __tablename__ = 'customer'
    __repr_fields__ = ['id', 'name', 'orgnr', 'trunks']
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    orgnr = db.Column(db.String())
    trunks = db.relationship('Trunk', secondary=lambda: customer_trunk_association)
    features = db.relationship('Feature', secondary=lambda: customer_feature_association) #lambda so association table config can be below classes due to read order


class Trunk(BaseModel):
    '''Write 'trunks.update()' to update trunks according to list'''
    __tablename__= 'trunk'
    __repr_fields__ = ['id', 'trunk', 'platform']
    id = db.Column(db.Integer(), primary_key=True)
    trunk = db.Column(db.String())
    platform = db.Column(db.String())
    customers = db.relationship('Customer', secondary=lambda: customer_trunk_association, back_populates='trunks')


class Feature(BaseModel):
    '''Keeps customer features in sync'''
    __tablename__= 'feature'
    __repr_fields__ = ['id', 'feature_id', 'feature_name']
    id = db.Column(db.Integer(), primary_key=True)
    feature_id = db.Column(db.String())
    feature_name = db.Column(db.String())
    customers = db.relationship('Customer', secondary=lambda: customer_trunk_association, back_populates='features')


customer_trunk_association = db.Table('customer_trunk_association',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('trunk_id', db.Integer, db.ForeignKey('trunk.id'))
    )

customer_feature_association = db.Table('customer_feature_association',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'))
    )
