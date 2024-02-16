import pyinputplus as pyip
from pathlib import Path
import os
import sys
import re

home = Path.home()
whole_target = Path(sys.argv[1])
target = str(whole_target.parts[0])
excludes = sys.argv[2:]
paths = []

def getPaths(root):
    for path in os.listdir(root):
            if os.path.isdir(root / path) == True:
                if re.search('^\.', path) or path == 'Library' or path in excludes:
                    continue
                if path == target:
                    if (root / whole_target).exists():
                        paths.append(root / whole_target)
                getPaths(root / path)
if whole_target == home:
    print(home)
elif whole_target.name == 'Library':
    print(home / 'Library')
else:
    getPaths(home)
    if len(paths) == 1:
        print(paths[0])
    elif len(paths) > 1:
        response = pyip.inputMenu([str(path) for path in paths], numbered=True)
        print(response)