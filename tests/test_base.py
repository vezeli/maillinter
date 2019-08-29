import pytest

from maillinter.base import Paragraph


@pytest.fixture
def paragraph_content():
    """Paragraph content without multiple subparagraphs."""
    clean_content = ("This is a basic test paragraph. The paragraph "
                     "contains several sentences of text which are "
                     "split over multiple lines. Also pay attention "
                     "there is no hard break in the paragraph "
                     "content.")
    dirty_content = ("  This is a  basic test   paragraph. The "
                     "paragraph  contains several  sentences of \t "
                     " text which are split over multiple lines.  Also"
                     " pay attention  there is \tno hard break in the "
                     "           \t\t     paragraph content.   ")
    return clean_content, dirty_content


@pytest.fixture
def paragraph_content_multiple(paragraph_content):
    """Paragraph content with multiple subparagraphs."""
    content = ("This is a dirty paragraph where we see that the "
               "contents is not linted.\nThere is also a subparagraph "
               "in this paragraph.")
    clean_content = paragraph_content[0] + "\n" + content

    content = ("  This is a dirty \t \t paragraph where   we see that "
               "the contents is not  \t  linted. \n There is also a "
               " subparagraph   in this   \t paragraph.  ")
    dirty_content = paragraph_content[1] + "\t \n  " + content

    wrapped_content = ("This is a basic test paragraph. The paragraph\n"
                       "contains several sentences of text which are\n"
                       "split over multiple lines. Also pay attention\n"
                       "there is no hard break in the paragraph\n"
                       "content.\n"
                       "This is a dirty paragraph where we see that the\n"
                       "contents is not linted.\n"
                       "There is also a subparagraph in this paragraph.")
    return clean_content, dirty_content, wrapped_content


def test_paragraph_text(paragraph_content):
    clean_content = paragraph_content[0]
    assert Paragraph(clean_content).clean_text == clean_content


def test_paragraph_repr_str(paragraph_content):
    clean_content = paragraph_content[0]
    paragraph = Paragraph(clean_content)
    repr_paragraph = "Paragraph('" + clean_content + "')"
    assert "{!r}".format(paragraph) == repr_paragraph
    assert print(paragraph.text) == print(clean_content)


def test_paragraph_clean(paragraph_content):
    clean_content = paragraph_content[0]
    dirty_content = paragraph_content[1]
    paragraph = Paragraph(dirty_content)
    assert paragraph.clean_text == clean_content


def test_paragraph_clean_multiple_subparagraphs(paragraph_content_multiple):
    clean_content = paragraph_content_multiple[0]
    dirty_content = paragraph_content_multiple[1]
    paragraph = Paragraph(dirty_content)
    assert paragraph.clean_text == clean_content


def test_paragraph_wrapped(paragraph_content_multiple):
    dirty_content = paragraph_content_multiple[1]
    wrapped_content = paragraph_content_multiple[2]
    paragraph = Paragraph(dirty_content)
    assert paragraph.wrap_text(47) == wrapped_content
