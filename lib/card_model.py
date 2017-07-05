"""Card model object.
"""


class Card(object):

    def __init__(self, **kwargs):
        self._gatherer_id = kwargs.get('gatherer_id')
        self._name = kwargs.get('name')
        self._card_number = kwargs.get('card_number')
        self._set_name = kwargs.get('set_name')
        self._set_code = kwargs.get('set_code')
        self._count = kwargs.get('count')

    @property
    def gatherer_id(self):
        return self._gatherer_id

    @property
    def name(self):
        return self._name

    @property
    def card_number(self):
        return self._card_number

    @property
    def set_name(self):
        return self._set_name

    @property
    def set_code(self):
        return self._set_code

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def __str__(self):
        return "{} {}, {} ({})".format(self.count, self.name, self.set_name, self.gatherer_id)
