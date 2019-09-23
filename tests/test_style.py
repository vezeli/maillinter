import pytest

from maillinter.style import re_uri


@pytest.fixture
def link_content():
    """Create a single link according to .md (`urn + url`)."""
    urn = "PhD Comics"
    url = "http://phdcomics.com/"
    return "".join(["(", urn, ")", "[", url, "]"]), urn, url


def test_url_regex_match(link_content):
    assert bool(re_uri.match(link_content[0])) == True


def test_url_regex_match_group(link_content):
    assert re_uri.match(link_content[0]).group("urn") == link_content[1]
    assert re_uri.match(link_content[0]).group("url") == link_content[2]


def test_url_regex_match_multiple_urls():
    """Test that the `re_uri` is not greedy."""
    content = (
        "I like (PhD Comics)[http://phdcomics.com/]. My favorite one "
        "is probably (this)"
        "[http://phdcomics.com/comics/archive.php?comicid=1296]."
    )
    assert len(re_uri.findall(content)) == 2
