#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import pytest
import utilotest

import rawmaker

run, failure = utilotest.create_cli_runner(rawmaker)

security = utilotest.register_marker('security')
font = utilotest.register_marker('font')

# do not skip ghost
ghost = pytest.mark.skipif(False, reason='require ghost')
