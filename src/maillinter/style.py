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

import re

RE_LINK = re.compile(
    r"""
    (?:\<(?P<g1>.+?)\>              # case 1: simple link
    |                               # case 2: annotated or reference link
    \[(?P<g2>.+?)\](?!:)            # match `g2` if not followed by `:`
    [ \t]*\n?[ \t]*                 # match a single broken line
    (?:\((?P<g3>.+?)\))?
    (?(g3)|(?:\[(?P<g4>.+?)\]))?    # match `g4` if no `g3`
    )
    """,
    re.VERBOSE,
)


def getLink(m):
    if m.group("g1"):
        anchor, url, ref = ("", m.group("g1"), "")
    elif not m.group("g1"):
        if m.group("g2") and m.group("g3"):
            anchor, url, ref = (m.group("g2"), m.group("g3"), "")
        elif m.group("g2") and m.group("g4"):
            anchor, url, ref = (m.group("g2"), "", m.group("g4"))
        elif m.group("g2") and not (m.group("g3") and m.group("g4")):
            anchor, url, ref = ("", "", m.group("g2"))
    return anchor, url, ref
