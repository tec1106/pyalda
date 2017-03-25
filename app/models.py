
class Base(object):
    def __init__(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)
    def update(self, **kwargs): #TODO: Remember ID
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)
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

class Customer(Base):
    __repr_fields__ = ['name', 'orgnr']
    pass

