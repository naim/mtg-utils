include "common";

def avgCMC:
    [.[].cmc | values]
    | add /length;

def avgCMCBySet($set):
    selectCardsBySet($set)
    | avgCMC;

def avgCMCByFormat($format):
    selectCardsByFormat($format)
    | avgCMC;
