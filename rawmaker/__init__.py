#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The rawmaker converts pdf to kiwi-internal project format

Hint: Pay attention to the public API on this file!
      Breaking changes are breaking!
"""

import os

import rawmaker.__patch__

__version__ = '2.10.3'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FEATURE_PATH = os.path.join(ROOT, 'rawmaker/features')

PROCESS = 'rawmaker'

assert os.path.exists(FEATURE_PATH)
