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


def getLink(m):
    if m.group("g1"):
        anchor, url, ref = ("", m.group("g1"), "")
    elif not m.group("g1"):
        if m.group("g2") and m.group("g3"):
            anchor, url, ref = (m.group("g2"), m.group("g3"), "")
        elif m.group("g2") and m.group("g4"):
            anchor, url, ref = (m.group("g2"), "", m.group("g4"))
        elif m.group("g2") and not (m.group("g3") and m.group("g4")):
            anchor, url, ref = ("", "", m.group("g2"))
    return anchor, url, ref
