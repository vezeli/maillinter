import re

re_link = re.compile(
    r"""
    \((?P<anchor>.*?)\)
    \[(?P<url>.*?)\]
    """,
    re.VERBOSE,
)


def gen_links(text):
    for link in re_link.finditer(text):
        yield link.group("anchor"), link.group("url")
