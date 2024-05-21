from pathlib import Path

# Files to write
python = """import pyinputplus as pyip
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
                if re.search(r'^\\.', path) or path == 'Library' or path in excludes:
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
        print(response)"""
cwd = Path.cwd()
zsh = f"""

# Quick-cd script, to quickly search and change to the desired directory, simply run in terminal:
# qcd Optional-parents/my-dir-name Optional-excluded-directory
# quick-cd.py is at {cwd}
function qcd() {{
    cd {cwd}
    result=$(python3 quick-cd.py "$@" | tee /dev/tty | sed -n -e '/^$/!h' -e '$x;$p') # Assign output to var, print it on screen, remove prompt
    if [[ -n $result ]]; then  # Check if result is not empty
        cd $result  # Use the output to change directory
    else
        cd - > /dev/null # Change to the original directory, prevent printing to terminal
        echo "No directory found"
    fi
}}"""
# Writing files
with open("quick-cd.py", "w") as python_script:
    python_script.write(python)
with open(Path.home() / ".zshrc", "r") as zsh_script_read:
    text = zsh_script_read.read()
    if text.find(zsh) == -1:
        with open(Path.home() / ".zshrc", "a") as zsh_script_append:
            zsh_script_append.write(zsh)
