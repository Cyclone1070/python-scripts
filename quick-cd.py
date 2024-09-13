import os
import re
import sys
from pathlib import Path

import pyinputplus as pyip

home = Path.home()
whole_target = Path(sys.argv[1])
target = str(whole_target.parts[0])
excludes = sys.argv[2:]
paths = []


def get_paths(root):
    for path in os.listdir(root):
        if os.path.isdir(root / path) is True:
            if re.search(r"^\.", path) or path == "Library" or path in excludes:
                continue
            if path == target:
                if (root / whole_target).exists():
                    paths.append(root / whole_target)
            get_paths(root / path)


if whole_target == home:
    print(home)
elif whole_target.name == "Library":
    print(home / "Library")
else:
    get_paths(home)
    if len(paths) == 1:
        print(paths[0])
    elif len(paths) > 1:
        response = pyip.inputMenu([str(path) for path in paths], numbered=True)
        print(response)
