"""Card collection objects.
"""

import csv
import yaml
import os.path
from contextlib import contextmanager

from card_model import Card


@contextmanager
def atomic_write(filepath, binary=False, fsync=False):
    """Writeable file object that atomically updates a file (using a temporary file).

    :param filepath: the file path to be opened
    :param binary: whether to open the file in a binary mode instead of textual
    :param fsync: whether to force write the file to disk
    """

    tmppath = filepath + '~'
    while os.path.isfile(tmppath):
        tmppath += '~'
    try:
        with open(tmppath, 'wb' if binary else 'w') as file:
            yield file
            if fsync:
                file.flush()
                os.fsync(file.fileno())
        os.rename(tmppath, filepath)
    finally:
        try:
            os.remove(tmppath)
        except (IOError, OSError):
            pass


class CardCollection(object):

    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', 0)
        self.cards = {}

    # TODO handle merging
    def set_cards(self, cards):
        if not isinstance(cards, dict):
            raise Exception("cards must be dict")

        if len(self.cards) > 0:
            for gid, card in cards.iteritems():
                if gid in self.cards:
                    self.cards[gid].count += 1
                else:
                    self.cards[gid] = card
        else:
            self.cards = cards

    def read(self, filename):
        if not os.path.isfile(filename):
            if self.verbose > 2:
                print self.__class__.__name__, "attempted to read", filename
            return

        if self.verbose > 2:
            print self.__class__.__name__, "read", filename

        with open(filename, mode='r') as f:
            self.parse(f)

    def write(self, filename):
        if self.verbose > 2:
            print self.__class__.__name__, "write", filename

        with atomic_write(filename) as f:
            self.serialize(f)


class ScryGlassCollection(CardCollection):

    def __init__(self, **kwargs):
        super(ScryGlassCollection, self).__init__(**kwargs)

    def parse(self, file):
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            if self.verbose > 2:
                print row

            gatherer_id = row[5]
            c = Card(gatherer_id=gatherer_id, name=row[1], card_number=row[3], set_name=row[2], set_code=row[4], count=int(row[0]))
            self.cards[gatherer_id] = c

        if self.verbose > 1:
            for gid, card in self.cards.iteritems():
                print card

    def serialize(self, file):
        writer = csv.writer(file)
        writer.writerow(["Count", "Name", "Edition", "Card Number", "Set Code", "ID"])

        for gid, card in self.cards.iteritems():
            writer.writerow([card.count, card.name, card.set_name, card.card_number, card.set_code, card.gatherer_id])


class DeckedCollection(CardCollection):

    def __init__(self, **kwargs):
        super(DeckedCollection, self).__init__(**kwargs)

    def parse(self, file):
        collection = yaml.load(file)

        for item in collection['doc'][1]['items']:
            if self.verbose > 2:
                print item

            gatherer_id = item[0]['id']
            c = Card(gatherer_id=gatherer_id, count=int(item[1]['r']))
            self.cards[gatherer_id] = c

        if self.verbose > 1:
            for gid, card in self.cards.iteritems():
                print card

    def serialize(self, file):
        collection = {
            'doc': [
                {'version': 1},
                {'items': None}
            ]}

        collection['doc'][1]['items'] = [[{'id': card.gatherer_id}, {'r': card.count}] for gid, card in self.cards.iteritems()]
        yaml.dump(collection, file, indent=2)
