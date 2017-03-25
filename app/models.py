

class Customer(object):
    def __init__(self, name, orgnr):
        self.name = name
        self.orgnr = orgnr
    def update(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __repr__(self):
        return "<Customer object; name={}, orgnr={}>".format(self.name, self.orgnr)


def printstuff(**kwargs):
    print("kwargs: ",kwargs)
    print("*kwargs: ",*kwargs)
    print("**kwargs: ",**kwargs)
    for key, value in kwargs.items():
        print(key, value)

stuff = {'foo':'bar'}
