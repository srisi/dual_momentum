import datetime
import os
import time
from pathlib import Path

import pytz

EASTERN = pytz.timezone('US/Eastern')

def file_exists_and_less_than_1hr_old(file_path: Path) -> bool:
    """Returns True if a file exists at the path and is less than 1 hour old."""

    if file_path.exists() and (time.time() - os.path.getmtime(str(file_path)) < 3600):
        return True
    else:
        return False

def file_exists_and_is_from_today(file_path: Path) -> bool:
    """
    Returns True if a file exists at the path and the file is from today.

    Uses EASTERN timezone as that's the relevant timezone for US stocks.

    """

    if file_path.exists():

        date = datetime.datetime.fromtimestamp(os.path.getmtime(str(file_path)))
        date = date.astimezone(EASTERN)
        today = datetime.datetime.today()
        if date.year == today.year and date.month == today.month and date.day == today.day:
            return True

