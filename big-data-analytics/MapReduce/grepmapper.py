#!/usr/bin/env python
import os
import sys
import re

SEARCH_STRING = os.environ["SEARCH_STRING"]

for line in sys.stdin:
    q = line.split("=")
    if bool(re.search(SEARCH_STRING, q[1])):
        doc_name = q[0].strip()
        print doc_name
