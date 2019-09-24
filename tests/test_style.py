import pytest

from maillinter.style import re_link


@pytest.fixture
def link_content():
    """Create a test link according to .md syntax (`anchor + url`)."""
    anchor = "PhD Comics"
    url = "http://phdcomics.com/"
    return "".join(["(", anchor, ")", "[", url, "]"]), anchor, url


def test_url_regex_match(link_content):
    assert bool(re_link.match(link_content[0])) == True


def test_url_regex_match_group(link_content):
    assert re_link.match(link_content[0]).group("anchor") == link_content[1]
    assert re_link.match(link_content[0]).group("url") == link_content[2]


def test_url_regex_match_multiple_urls():
    """Test that `re_link` is not greedy."""
    content = (
        "I like (PhD Comics)[http://phdcomics.com/]. My favorite one "
        "is probably (this)"
        "[http://phdcomics.com/comics/archive.php?comicid=1296]."
    )
    assert len(re_link.findall(content)) == 2
