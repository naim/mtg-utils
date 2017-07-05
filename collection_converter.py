#!/usr/bin/env python

"""Take different MTG card collection formats and convert them to other formats.
Primarily used for going from ScryGlass csv list to Decked Builder coll2 format.
"""

__author__ = "Naim Falandino"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse

from lib.card_collection import ScryGlassCollection, DeckedCollection


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
        if args.merge:
            out_collection.read(args.out_filename)
        out_collection.set_cards(in_collection.cards)
        out_collection.write(args.out_filename)
    else:
        print "No output collection specified."


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
