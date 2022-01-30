#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The rawmaker converts pdf to kiwi-internal project format

Hint: Pay attention to the public API on this file!
      Breaking changes are breaking!
"""

import os

import configo

# pylint:disable=W0613
import rawmaker.__patch__
from rawmaker.parameter import LAYOUT
from rawmaker.parameter import ONELINE

__version__ = '2.31.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'rawmaker'

configo.cloud_lookup(PROCESS)
