import pytest

from maillinter.form import RE_LINK, link_metadata


def test_link_regex_match_simple_link():
    assert bool(RE_LINK.match("<https://www.linux.org/>")) == True


def test_link_regex_match_annotated_link():
    assert bool(RE_LINK.match("[Linux](https://www.linux.org/)")) == True


def test_link_regex_match_reference_link():
    assert bool(RE_LINK.match("[Linux]")) == True


def test_link_regex_match_annotated_reference_link():
    assert bool(RE_LINK.match("[HHGTTH][42]")) == True


def test_link_regex_skip_pure_reference():
    assert bool(RE_LINK.match("[42]:")) == False


def test_link_regex_match_multiple_urls():
    content = (
        "Multiple links [Python](https://www.python.org/) and "
        "<https://www.linux.org/>."
    )
    assert len(RE_LINK.findall(content)) == 2


def test_link_regex_match_is_not_greedy():
    content = "Both [Python] and [Linux] take a lot of my time."
    assert len(RE_LINK.findall(content)) == 2


def test_parse_re_match_simple_link():
    content = "This is a simple link <https://www.python.org/>."
    match = RE_LINK.search(content)
    assert link_metadata(match) == ("", "https://www.python.org/", "")


def test_parse_re_match_annotated_link():
    content = "This is an annotated link [Python](https://www.python.org/)."
    match = RE_LINK.search(content)
    assert link_metadata(match) == ("Python", "https://www.python.org/", "")


def test_parse_re_match_reference_link():
    content = "This is a reference link [Python]."
    match = RE_LINK.search(content)
    assert link_metadata(match) == ("", "", "Python")


def test_parse_re_match_annotated_reference_link():
    content = "This is a simple link [HHGTTH][42]."
    match = RE_LINK.search(content)
    assert link_metadata(match) == ("HHGTTH", "", "42")


# TODO: test that RE works for half nested brackets, e.g., [ [](]) or []([]) and
#      try to improve
# TODO: make different exclussion of : in reference links because look-ahead can
#      make truble in links like "[] is :"
