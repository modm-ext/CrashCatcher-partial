# Script is tested on OS X 10.12
# YOUR MILEAGE MAY VARY

import sys
import shutil
import fnmatch
import subprocess
from pathlib import Path

source_paths = {
    "CrashCatcher": [
        "README.creole",
        "Core/src/",
        "include/CrashCatcher.h",
    ],
    "CrashDebug": [
        "README.creole",
        "bins/"
    ]
}

# clone the repository
for repo in source_paths:
    if not Path(f"{repo}_src").exists():
        print(f"Cloning {repo} repositories...")
        subprocess.run(f"git clone https://github.com/adamgreen/{repo}.git {repo}_src", shell=True)

    # remove the sources in this repo
    if Path(repo).exists():
        shutil.rmtree(repo)

    print(f"Copying {repo} sources...")
    for pattern in source_paths[repo]:
        for path in Path(f"{repo}_src").glob(pattern):
            dest = Path(repo) / path.relative_to(f"{repo}_src")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                shutil.copytree(path, dest)
            else:
                shutil.copy2(path, dest)

print("Normalizing CrashCatcher newlines and whitespace...")
subprocess.run("sh ./post_script.sh > /dev/null 2>&1", shell=True)
