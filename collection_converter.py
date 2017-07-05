#!/usr/bin/env python

"""
collection_converter.py

Take different MTG card collection formats and convert them to other formats. Primarily
used for going from ScryGlass CSV list to Decked Builder coll2 format.
"""

__author__ = "Naim Falandino"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import yaml
import csv


class CardCollection(object):

    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', 0)
        self.cards = {}

    # TODO handle merging
    def set_cards(self, cards):
        if not isinstance(cards, dict):
            raise Exception("cards must be dict")

        if len(self.cards) > 0:
            return
        else:
            self.cards = cards

    def read(self, filename):
        if self.verbose > 2:
            print self.__class__.__name__, filename

        with open(filename, mode='r') as f:
            self.parse(f)

    def write(self, filename):
        if self.verbose > 2:
            print self.__class__.__name__, filename

        with open(filename, mode='w') as f:
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
            c = Card(gatherer_id=gatherer_id, name=row[1], card_number=row[3], set_name=row[2], set_code=row[4], count=row[0])
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
            c = Card(gatherer_id=gatherer_id, count=item[1]['r'])
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


def create_collection(collection_type, verbose):
    if collection_type == "scryglass":
        return ScryGlassCollection(verbose=verbose)
    elif collection_type == "decked":
        return DeckedCollection(verbose=verbose)
    else:
        raise Exception("collection_type not defined")


def main(args):
    if args.verbose > 1:
        print args

    in_collection = create_collection(args.from_type, args)
    in_collection.read(args.in_filename)

    if args.to_type and args.out_filename:
        out_collection = create_collection(args.to_type, args)
        # TODO
        if args.merge:
            out_collection.read(args.out_filename)
        out_collection.set_cards(in_collection.cards)
        out_collection.write(args.out_filename)


if __name__ == "__main__":
    valid_types = ["decked", "scryglass"]

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", dest="in_filename", required=True)
    parser.add_argument("-o", "--out", action="store", dest="out_filename", required=False)

    parser.add_argument("-f", "--from", action="store", dest="from_type", required=True,
                        help="A valid collection type to convert from. Valid types: {}".format(', '.join(valid_types)))
    parser.add_argument("-t", "--to", action="store", dest="to_type", required=False,
                        help="A valid collection type to convert to. Valid types: {}".format(', '.join(valid_types)))

    parser.add_argument("-m", "--merge", action="store_true",
                        help="Merge output with destination collection.")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
