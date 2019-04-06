#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os import listdir
from os.path import join
from sys import modules

from utila import file_create

from rawmaker import FEATURE_PATH
from rawmaker.features import features
from rawmaker.features import find_features
from rawmaker.features import load_features


def test_find_features():
    features = find_features(FEATURE_PATH)
    assert len(features)


def test_feature_interface():
    """Ensure that given features have a valid interface"""
    # ignore __pycache__ and __init__.py
    IGNORE__INIT__ = 1
    python_files_in_feature_path = len([
        item for item in listdir(FEATURE_PATH) if item.endswith('.py')
    ]) - IGNORE__INIT__

    working_features = features(FEATURE_PATH)
    assert len(working_features) == python_files_in_feature_path


# Minimal feature header
FEATURE = """\
def commandline():
    pass

def work():
    pass
"""


def test_load_features(tmpdir):
    """Test loading feature dure:

    Testprocess:
        1. Create minimal feature
        2. Load feature
        3. Determine the difference of module to get feature count
    """
    # create minimal feature
    feature_file = join(tmpdir, 'masterfeature.py')
    file_create(feature_file, FEATURE)

    # determine current modules
    modules_before = set(modules)

    # find and load features
    features = find_features(tmpdir)
    failure = load_features(tmpdir, features)
    assert not failure

    # determine new modules
    modules_after = set(modules)

    modules_loaded = len(modules_after - modules_before)

    assert modules_loaded == len(features)
