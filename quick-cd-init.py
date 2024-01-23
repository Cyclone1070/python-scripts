from pathlib import Path

# Files to write
python = '''import pyinputplus as pyip
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
if target == str(home):
    print(home)
elif target == 'Library':
    print(home / 'Library')
else:
    getPaths(home)
    if len(paths) == 1:
        print(paths[0])
    elif len(paths) > 1:
        response = pyip.inputMenu([str(path) for path in paths], numbered=True)
        print(response)'''
cwd = Path.cwd()
zsh = f'''

# Quick-cd script, to quickly search and change to the desired directory, simply run in terminal:
# qcd Optional-parents/my-dir-name Optional-excluded-directory
# quick-cd.py is at {cwd}
function qcd() {{
    cd {cwd}
    result=$(python3 quick-cd.py "$@" | tee /dev/tty | sed -n -e '/^$/!h' -e '$x;$p') # Assign output to var, print it on screen, remove prompt
    if [[ -n $result ]]; then  # Check if result is not empty
        cd $result  # Use the output to change directory
    else
        _trash=$(cd -) # Change to the original directory, prevent printing to terminal
        echo "No directory found"
    fi
}}'''
# Writing files
py_script = open('quick-cd.py', 'w')
py_script.write(python)
py_script.close()
zsh_script = open(Path.home() / '.zshrc')
text = zsh_script.read()
zsh_script.close()
if text.find(zsh) == -1:
    zsh_script = open(Path.home() / '.zshrc', 'a')
    zsh_script.write(zsh)
    zsh_script.close()