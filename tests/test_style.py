# Copyright 2019 Velibor Zeli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
