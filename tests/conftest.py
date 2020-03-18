# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import utila

import tests.resources
import tests.resources.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

def pytest_sessionstart(session):  # pylint:disable=W0613
    if 'PYTEST_XDIST_WORKER' in os.environ:
        # master process only
        return

    single_test = '-k' in sys.argv
    if not single_test and ('GENERATE' in os.environ or utila.test.LONGRUN):

        utila.log('install requirements')
        tests.resources.update.install_requirements()

        # ensure that all test resources exists
        utila.log('synchronize test resources')
        tests.resources.update.sync_resources()

        utila.log('extract resources')
        tests.resources.update.extract_examples()

    for item in tests.resources.REQUIRED_RESOURCES:
        advice = 'run `baw --test=generate` to generate test data'
        msg = f'required test path does not exists: {item}, {advice}'
        assert os.path.exists(item), msg
