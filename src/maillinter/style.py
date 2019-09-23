import re

re_uri = re.compile(r'''
        \((?P<urn>.*?)\)
        \[(?P<url>.*?)\]
        ''', re.VERBOSE)
