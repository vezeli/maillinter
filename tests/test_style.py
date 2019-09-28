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

from maillinter.style import link_pattern


@pytest.fixture
def link_content():
    """Create a test link according to .md syntax (`anchor + url`)."""
    anchor = "PhD Comics"
    url = "http://phdcomics.com/"
    return "".join(["[", anchor, "]", "(", url, ")"]), anchor, url


def test_url_regex_match(link_content):
    assert bool(link_pattern.match(link_content[0])) == True


def test_url_regex_match_group(link_content):
    assert link_pattern.match(link_content[0]).group("g2") == link_content[1]
    assert link_pattern.match(link_content[0]).group("g3") == link_content[2]


def test_url_regex_match_multiple_urls():
    """Test that `link_pattern` is not greedy."""
    content = (
        "I like [PhD Comics](http://phdcomics.com/). My favorite one "
        "is probably [this]"
        "(http://phdcomics.com/comics/archive.php?comicid=1296)."
    )
    assert len(link_pattern.findall(content)) == 2
