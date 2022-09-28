#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import ghost as gs
import pytest
import utilatest

import rawmaker

run, failure = utilatest.create_cli_runner(rawmaker)

security = utilatest.register_marker('security')
font = utilatest.register_marker('font')

# do not skip ghost
ghost = pytest.mark.skipif(False, reason='require ghost')
