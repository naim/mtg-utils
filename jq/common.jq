##
# Common selection/find functions with AllSets-x.json

def cleanCards:
    .[]
    | del(
        .artist,
        .border,
        .foreignNames,
        .hand,
        .id,
        .imageName,
        .layout,
        .legalities,
        .life,
        .mciNumber,
        .multiverseid,
        .names,
        .number,
        .originalType,
        .originalText,
        .printings,
        .rarity,
        .releaseDate,
        .reserved,
        .rulings,
        .source,
        .starter,
        .timeshifted,
        .variations,
        .watermark);

def uniqueCardsByName:
    flatten
    | unique_by(.name);

def selectCards:
    [.cards[]];


##
# Card filtering by field

def filterCardsByName($name):
    [.[]
    | select(contains({name: $name}))];

def filterCardsByNames($names):
    [.[]
    | select(contains({names: $names}))];

def filterCardsByType($type):
    [.[]
    | select(contains({type: $type}))];

def filterCardsByTypes($types):
    [.[]
    | select(contains({types: $types}))];

def filterCardsBySubTypes($subtypes):
    [.[]
    | select(contains({subtypes: $subtypes}))];

def filterCardsByText($text):
    [.[]
    | select(contains({text: $text}))];

def filterCardsByColors($colors):
    [.[]
    | select(contains({colors: $colors}))];

def filterCardsByColorIdentity($colorIdentity):
    [.[]
    | select(contains({colorIdentity: $colorIdentity}))];


##
# Set and Block selection

def selectSet($set):
    .[]
    | select(.code == $set);

def selectBlock($block):
    .[]
    | select(.block == $block);


##
# Card selection functions

def selectAllCards:
    .[]
    | selectCards;

def selectCardsBySetType($setType):
    .[]
    | select(.type == $setType)
    | selectCards;

def selectCardsBySet($set):
    .[]
    | select(.code == $set)
    | selectCards;

def selectCardsByBlock($block):
    .[]
    | select(.block == $block)
    | selectCards;

def selectCardsByFormat($format):
    [selectAllCards
    | .[]
    | select(.legalities[] |
        (.format == $format and .legality == "Legal"))?]
    | uniqueCardsByName;

def selectCardsByName($name):
    [selectAllCards
    | filterCardsByName($name)]
    | uniqueCardsByName;

def selectCardsByNames($names):
    [selectAllCards
    | filterCardsByNames($names)]
    | uniqueCardsByName;

def selectCardsByType($type):
    [selectAllCards
    | filterCardsByType($type)]
    | uniqueCardsByName;

def selectCardsByTypes($types):
    [selectAllCards
    | filterCardsByTypes($types)]
    | uniqueCardsByName;

def selectCardsBySubTypes($subtypes):
    [selectAllCards
    | filterCardsBySubTypes($subtypes)]
    | uniqueCardsByName;

def selectCardsByText($text):
    [selectAllCards
    | filterCardsByText($text)]
    | uniqueCardsByName;
