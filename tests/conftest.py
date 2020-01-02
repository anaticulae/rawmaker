# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

from rawmaker import ROOT
from tests.resources import RESOURCES

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

# TODO: Ensure that tests waits before this process is ready

if not 'PYTEST_XDIST_WORKER' in os.environ:
    # master process only
    # ensure to avoid race condition if more than one thread tries to
    # install or use rawmaker
    if utila.test.LONGRUN:
        utila.clean_install(ROOT, 'rawmaker')

        completed = utila.run('power --all', RESOURCES)  # pylint:disable=C0103
        assert completed.returncode == utila.SUCCESS, str(completed)
