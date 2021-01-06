# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import linero.__patch__
import rawmaker

__version__ = rawmaker.__version__
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FEATURE_PATH = os.path.join(ROOT, 'linero/features')

PROCESS = 'linero'

DESCRIPTION = """\
Linero converts a bunch of lines to the following possible features:

* tables
* figures/diagrams
* horizontal lines
"""

assert os.path.exists(FEATURE_PATH), FEATURE_PATH
