import re

RE_LINK = re.compile(
    r"""
    (?:\<(?P<g1>.+?)\>              # case 1: simple link
    |                               # case 2: annotated or reference link
    \[(?P<g2>.+?)\](?!:)            # match `g2` if not followed by `:`
    [ \t]*\n?[ \t]*                 # match a single broken line
    (?:\((?P<g3>.+?)\))?
    (?(g3)|(?:\[(?P<g4>.+?)\]))?    # match `g4` if no `g3`
    )
    """,
    re.VERBOSE,
)


def link_metadata(match):
    try:
        groups = match.groups(default="")
    except AttributeError:
        groups = match

    return _translate_groups(*groups)


def _translate_groups(group1, group2, group3, group4):
    if group1:
        anchor, address, reference = ("", group1, "")
    elif not group1:
        if group2 and group3:
            anchor, address, reference = (group2, group3, "")
        elif group2 and group4:
            anchor, address, reference = (group2, "", group4)
        elif group2 and not (group3 and group4):
            anchor, address, reference = ("", "", group2)
    return anchor, address, reference
