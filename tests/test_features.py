#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from os import listdir

from rawmaker import FEATURE_PATH
from rawmaker.features import find_features


def test_feature_interface():
    """Ensure that given features have a valid interface"""
    # ignore __pycache__
    python_files_in_feature_path = len(
        [item for item in listdir(FEATURE_PATH) if item.endswith('.py')])
    # ignore __init__
    python_files_in_feature_path = python_files_in_feature_path - 1

    working_features = find_features(FEATURE_PATH)
    assert len(working_features) == python_files_in_feature_path


def test_find_corrupted_feature(testdir, capsys, monkeypatch):
    testdir.makefile(".py", corrupted_feature="# Empty")
    result = []

    with monkeypatch.context() as context:
        context.setattr('importlib.import_module', lambda _, __: object())
        result = find_features(str(testdir))
    assert result == []

    output, err = capsys.readouterr()
    assert 'SKIP' in output + err


# Minimal feature header
FEATURE = """\
def commandline():
    pass

def work():
    pass
"""
