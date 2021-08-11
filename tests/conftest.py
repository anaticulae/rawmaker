# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import genex
import power
import pytest
import utila

import rawmaker
import tests.resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = rawmaker.PROCESS
WORKER = 6

power.setup(rawmaker.ROOT)

RESOURCES = [
    (power.BACHELOR056_PDF, '0:34'),
    (power.BACHELOR051_PDF, '25:35'),
    (power.BOOK007_PDF, None),
    (power.DOCU13_PDF, None),
    (power.BACHELOR090_PDF, '76:81'),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.HOME040_PDF, None),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER098_PDF, '53:61'),
    (power.MASTER112_PDF, '110'),
    (power.BACHELOR063_PDF, '24:28'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.REQUIRED_RESOURCES)


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        oneline=None,
        pdfinfo=False,
        linero=False,
        worker=WORKER,
        base=power.REPOSITORY,
    )


# yapf:disable
RESOURCES_SCALED = [
    (tests.resources.FONTS_SCALED_PDF, ('sel page_0.text_5_487', 'page0_first')),
    (tests.resources.FONTS_SCALED_PDF, ('sel page_0.text_490_950', 'page0_second')),
    (tests.resources.FONTS_SCALED_PDF, ('sel page_1.text_5_632', 'page1_first')),
]
# yapf:enable


def extract_scaled(resources):
    dest = power.generated(folder='scaled')
    if os.path.exists(dest):
        return
    os.makedirs(dest)
    for source, (script, name) in resources:
        outpath = os.path.join(dest, f'{name}.pdf')
        tmp = utila.tmpfile(power.ROOT)
        utila.file_replace(tmp, script)
        utila.run(f'jam -i {source} --script {tmp} -o {outpath}')


def validate_scaled(_):  # pylint:disable=W0613
    # disable page number validation
    pass
