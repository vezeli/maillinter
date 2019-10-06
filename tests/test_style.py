import pytest

from maillinter.style import RE_LINK, getLink


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


def test_getLink_simple_link():
    content = "This is a simple link <https://www.python.org/>."
    match = RE_LINK.search(content)
    assert getLink(match) == ("", "https://www.python.org/", "")


def test_getLink_annotated_link():
    content = "This is an annotated link [Python](https://www.python.org/)."
    match = RE_LINK.search(content)
    assert getLink(match) == ("Python", "https://www.python.org/", "")


def test_getLink_reference_link():
    content = "This is a reference link [Python]."
    match = RE_LINK.search(content)
    assert getLink(match) == ("", "", "Python")


def test_getLink_annotated_reference_link():
    content = "This is a simple link [HHGTTH][42]."
    match = RE_LINK.search(content)
    assert getLink(match) == ("HHGTTH", "", "42")
