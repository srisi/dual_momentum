import os
import time
from pathlib import Path

def file_exists_and_less_than_1hr_old(file_path: Path) -> bool:
    """
    Returns True if a file exists at the path and is less
    than 1 hour old
    :param file_path: Path
    :return: bool
    """
    if file_path.exists():
        print(time.time() - os.path.getmtime(str(file_path)))

    if file_path.exists() and (time.time() - os.path.getmtime(str(file_path)) < 3600):
        return True
    else:
        return False
