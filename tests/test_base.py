import pytest

from maillinter.base import Paragraph, Link


@pytest.fixture
def paragraph_content():
    """Paragraph content with single subparagraph."""
    clean_content = (
        "This is a basic test paragraph. The paragraph "
        "contains several sentences of text which are "
        "split over multiple lines. Also pay attention "
        "there is no hard break in the paragraph "
        "content."
    )
    dirty_content = (
        "  This is a  basic test   paragraph. The "
        "paragraph  contains several  sentences of \t "
        " text which are split over multiple lines.  Also"
        " pay attention  there is \tno hard break in the "
        "           \t\t     paragraph content.   "
    )
    return clean_content, dirty_content


@pytest.fixture
def paragraph_content_multiple(paragraph_content):
    """Paragraph content with multiple subparagraphs."""
    content = (
        "This is a dirty paragraph where we see that the "
        "contents is not linted.\nThere is also a subparagraph "
        "in this paragraph."
    )
    clean_content = paragraph_content[0] + "\n" + content

    content = (
        "  This is a dirty \t \t paragraph where   we see that "
        "the contents is not  \t  linted. \n There is also a "
        " subparagraph   in this   \t paragraph.  "
    )
    dirty_content = paragraph_content[1] + "\t \n  " + content

    wrapped_content = (
        "This is a basic test paragraph. The paragraph\n"
        "contains several sentences of text which are\n"
        "split over multiple lines. Also pay attention\n"
        "there is no hard break in the paragraph\n"
        "content.\n"
        "This is a dirty paragraph where we see that the\n"
        "contents is not linted.\n"
        "There is also a subparagraph in this paragraph."
    )

    double_space_wrapped_content = (
        "This is a basic test paragraph.  The paragraph\n"
        "contains several sentences of text which are\n"
        "split over multiple lines.  Also pay attention\n"
        "there is no hard break in the paragraph\n"
        "content.\n"
        "This is a dirty paragraph where we see that the\n"
        "contents is not linted.\n"
        "There is also a subparagraph in this paragraph."
    )
    return clean_content, dirty_content, wrapped_content, double_space_wrapped_content


@pytest.fixture
def paragraph_content_multiple_links():
    content = (
        "I enjoy reading (PhD Comics)[http://phdcomics.com/]. "
        "If you like them as well, you should definitely check out "
        "(this one)[http://phdcomics.com/comics/archive.php?comicid=1296]."
    )
    return content


def test_default_Paragraph_single_subparagraph_text(paragraph_content):
    clean_content = paragraph_content[0]
    assert Paragraph(clean_content).clean_text == clean_content


def test_default_Paragraph_single_subparagraph_str_repr(paragraph_content):
    clean_content = paragraph_content[0]
    paragraph = Paragraph(clean_content)
    repr_paragraph = f"Paragraph({clean_content!r}, 'common')"
    assert print(paragraph.text) == print(clean_content)
    assert "{!r}".format(paragraph) == repr_paragraph


def test_default_Paragraph_single_subparagraph_clean_text(paragraph_content):
    clean_content = paragraph_content[0]
    dirty_content = paragraph_content[1]
    paragraph = Paragraph(dirty_content)
    assert paragraph.clean_text == clean_content


def test_default_Paragraph_multiple_subparagraphs_clean_text(
    paragraph_content_multiple
):
    clean_content = paragraph_content_multiple[0]
    dirty_content = paragraph_content_multiple[1]
    paragraph = Paragraph(dirty_content)
    assert paragraph.clean_text == clean_content


def test_default_Paragraph_multiple_subparagraphs_wrap_text(paragraph_content_multiple):
    dirty_content = paragraph_content_multiple[1]
    wrapped_content = paragraph_content_multiple[2]
    paragraph = Paragraph(dirty_content)
    assert paragraph.wrap_text(width=47) == wrapped_content


def test_common_style_Paragraph_multiple_subparagraphs_wrap_text(
    paragraph_content_multiple
):
    dirty_content = paragraph_content_multiple[1]
    wrapped_content = paragraph_content_multiple[2]
    paragraph = Paragraph(dirty_content, style="common")
    assert paragraph.wrap_text(width=47) == wrapped_content


def test_monospaced_style_Paragraph_multiple_subparagraphs_wrap_text(
    paragraph_content_multiple
):
    dirty_content = paragraph_content_multiple[1]
    double_space_wrapped_content = paragraph_content_multiple[3]
    paragraph = Paragraph(dirty_content, style="monospaced")
    assert paragraph.wrap_text(width=47) == double_space_wrapped_content


def test_default_Paragraph_has_links(
    paragraph_content, paragraph_content_multiple_links
):
    paragraph_without_links = Paragraph(paragraph_content[0])
    paragraph_with_links = Paragraph(paragraph_content_multiple_links)
    assert paragraph_without_links.has_links == False
    assert paragraph_with_links.has_links == True


@pytest.mark.parametrize(
    "anchor, address, reference, expected_type",
    [
        ("", "https://www.python.org/", "", "s"),
        ("Python", "https://www.python.org/", "", "a"),
        ("", "", "Python", "r"),
        ("HHGTTH", "", "42", "A"),
    ],
)
def test_Link_types(anchor, address, reference, expected_type):
    d = dict()
    d["anchor"] = anchor
    d["address"] = address
    d["references"] = reference
    assert Link(d).type == expected_type
