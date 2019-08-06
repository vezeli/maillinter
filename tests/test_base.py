import pytest

import src.base as base


@pytest.fixture
def result_string():
    """Setup a dummy sentace."""
    return 'This is a test sentance.'


def test_lint_whitespace_from_beginning(result_string):
    test_string = '     This is a test sentance.'
    assert result_string == base.lint_text(test_string)


def test_lint_whitespace_from_end(result_string):
    test_string = 'This is a test sentance.     '
    assert result_string == base.lint_text(test_string)


def test_lint_whitespace_from_middle(result_string):
    test_string = 'This      is a  test    sentance.'
    assert result_string == base.lint_text(test_string)


def test_lint_whitespace_before_symbol(result_string):
    test_string = 'This is a test sentance  .'


def test_lint_different_whitespace_characters(result_string):
    test_string = ' \t\t This is \n\n a    \n \t test \t \n\t sentance\t.  '
    assert result_string == base.lint_text(test_string)
