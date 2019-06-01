import collections


ParagraphType = collections.namedtuple('ParagraphType', ('label', 'marker'))
HARD_RETURN = ParagraphType('HR', '\\\\')
LISTING = ParagraphType('Listing', '\n ')
TEXT = ParagraphType('Text', None)


def structure_parser(content, t):
    if t is HARD_RETURN.label:
        return content.replace(HARD_RETURN.marker, '\n')
    elif t is LISTING.label:
        return content.split(LISTING.marker)
    elif t is 'Mix':
        pass


def determine_type(par):
    if HARD_RETURN.marker in par.content:
        hard_return = True
    else:
        hard_return = False

    if LISTING.marker in par.content:
        listing = True
    else:
        listing = False

    if hard_return and not listing:
        return HARD_RETURN.label
    elif not hard_return and listing:
        return LISTING.label
    elif hard_return and listing:
        return 'Mix'
    elif not hard_return and not listing:
        return TEXT.label
    else:
        return None
