from datetime import datetime
from app import db

from sqlalchemy import Column, String, Integer

class BaseModel(object):
    __abstract__ = True
    __repr_fields__ = ['id']

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


class Customer(db.Model, BaseModel):
    __tablename__ = 'customer'
    __repr_fields__ = ['id', 'name', 'orgnr']
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    orgnr = Column(String())

