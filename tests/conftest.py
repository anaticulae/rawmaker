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

RESOURCES = [
    (power.MASTER072_PDF, None),
    (power.BACHELOR056_PDF, '14:34'),
    (power.BOOK007_PDF, None),
    (power.DOCU13_PDF, None),
    (power.BACHELOR090_PDF, '76:81'),
    (power.DOCU07_PDF, None),
    (power.MASTER098_PDF, '53:61'),
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
