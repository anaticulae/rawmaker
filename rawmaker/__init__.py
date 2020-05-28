#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The rawmaker converts pdf to kiwi-internal project format

Hint: Pay attention to the public API on this file!
      Breaking changes are breaking!
"""
import os

__version__ = '1.21.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FEATURE_PATH = os.path.join(ROOT, 'rawmaker/features')

PROCESS_NAME = 'rawmaker'

assert os.path.exists(FEATURE_PATH)
