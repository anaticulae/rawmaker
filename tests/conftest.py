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

PACKAGE = rawmaker.PROCESS

power.setup(rawmaker.ROOT)

RESOURCES = [
    (power.BACHELOR056_PDF, '0:34'),
    (power.BACHELOR051_PDF, '25:35'),
    (power.BOOK007_PDF, None),
    (power.DOCU13_PDF, None),
    (power.BACHELOR090_PDF, '76:81'),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER098_PDF, '53:61'),
    (power.BACHELOR063_PDF, '24:28'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.REQUIRED_RESOURCES)


def extract(resources):
    todo = [
        f'rawmaker -i {source} -o {power.link(source)} -j=8 --pages={strpages(pages)}'
        for source, pages in resources
    ]
    completed = utila.run_parallel(todo)
    assert completed == utila.SUCCESS


def strpages(item) -> str:
    if item is None:
        return ':'
    return item
