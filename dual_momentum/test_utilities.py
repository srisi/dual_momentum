import os
import time
from pathlib import Path

import pytest
from dual_momentum.utilities import file_exists_and_less_than_1hr_old


@pytest.mark.parametrize(
    'age_seconds, file_exists, expected_result', [
        (0, True, True),    # exists, new -> True
        (0, False, False),  # not exist -> False
        (3599, True, True), # exist, <3600 -> True
        (3600, True, False) # >3600 -> False
    ])
def test_file_exists_and_less_than_1hr_old(
    tmp_path, age_seconds, file_exists, expected_result, monkeypatch
):

    p = Path(tmp_path, 'test.txt')
    if file_exists:
        p.write_text('test')    # write to actually create the temp file if required

    def getmtime(*args):
        # -0.1 because test has some run time of its own, otherwise the 3600 test fails
        return time.time() - age_seconds - 0.1

    monkeypatch.setattr(os.path, 'getmtime', getmtime)

    result = file_exists_and_less_than_1hr_old(p)
    assert result == expected_result
