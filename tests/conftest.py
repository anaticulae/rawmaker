# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import rawmaker
import tests.resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = rawmaker.PROCESS_NAME

power.setup(rawmaker.ROOT)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.REQUIRED_RESOURCES)


def extract():
    todo = [
        (power.BOOK007_PDF, power.link(power.BOOK007_PDF), None),
        (power.DOCU13_PDF, power.link(power.DOCU13_PDF), None),
        (power.BACHELOR090_PDF, power.link(power.BACHELOR090_PDF), '76:81'),
    ]
    todo = [
        f'rawmaker -i {source} -o {dest} -j=8 --pages={strpages(pages)}'
        for source, dest, pages in todo
    ]
    completed = utila.run_parallel(todo)
    assert completed == utila.SUCCESS


def strpages(item) -> str:
    if item is None:
        return ':'
    return item
