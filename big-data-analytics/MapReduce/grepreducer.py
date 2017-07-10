#!/usr/bin/env python
import os
import sys

print os.environ["SEARCH_STRING"] + " found in the following documents:"
filenames = set()
for line in sys.stdin:
    filenames.add(line)
for name in filenames:
    print name[:2]
