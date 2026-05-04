# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
# import genex
import hoverpower
import pytest
import utilo
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import rawmaker
import tests.resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = rawmaker.PROCESS
WORKER = 6

hoverpower.setup(rawmaker.ROOT)

RESOURCES = [
    (hoverpower.BACHELOR051_PDF, '25:35'),
    (hoverpower.BACHELOR056_PDF, '0:34'),
    (hoverpower.BACHELOR063_PDF, '24:28'),
    (hoverpower.BACHELOR090_PDF, '76:81'),
    (hoverpower.DISS143_PDF, '27'),
    (hoverpower.MASTER072_PDF, '0:10'),
    (hoverpower.MASTER116_PDF, '18'),
    hoverpower.BOOK007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU013_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    setup_configos()
    hoverpower.run(tests.resources.REQUIRED_RESOURCES)


def extract(resources):
    pass
    # genex.extract(
    #     files=resources,
    #     dest=hoverpower.generated(),
    #     oneline=None,
    #     worker=WORKER,
    # )


# yapf:disable
RESOURCES_SCALED = [
    (tests.resources.FONTS_SCALED_PDF, ('sel page_0.text_5_487', 'page0_first')),
    (tests.resources.FONTS_SCALED_PDF, ('sel page_0.text_490_950', 'page0_second')),
    (tests.resources.FONTS_SCALED_PDF, ('sel page_1.text_5_632', 'page1_first')),
]
# yapf:enable


def extract_scaled(resources):
    dest = hoverpower.generated(folder='scaled')
    if os.path.exists(dest):
        return
    os.makedirs(dest)
    for source, (script, name) in resources:
        outpath = os.path.join(dest, f'{name}.pdf')
        tmp = utilo.tmpfile(hoverpower.ROOT)
        utilo.file_replace(tmp, script)
        utilo.run(f'jam -i {source} --script {tmp} -o {outpath}')


def validate_scaled(_):  # pylint:disable=W0613
    # disable page number validation
    pass


RESOURCES_SHORTEN = [
    (hoverpower.MASTER105_PDF, '86 87'),
]


def extract_shorten(resources):
    dest = hoverpower.generated(folder='shorten')
    if os.path.exists(dest):
        return
    os.makedirs(dest)
    for source, pages in resources:
        filename = utilo.file_name(source)
        outpath = os.path.join(dest, f'{filename}.pdf')
        utilo.run(f'pdfcat {source} {pages} > {outpath}')


def validate_shorten(_):  # pylint:disable=W0613
    # disable page number validation
    pass


CONFIGOS = os.path.join(rawmaker.ROOT, 'tests/resources/configos')

NAMES = ['rawmaker']


def setup_configos():
    os.makedirs(CONFIGOS, exist_ok=True)
    for name in NAMES:
        config = os.path.join(CONFIGOS, f'{name}.hv')
        if not os.path.exists(config):
            utilo.log(f'generate hv config: {name}')
            source = os.path.join(rawmaker.ROOT, name)
            utilo.run(f'configos --generate -i {source} >> {config}')
    configos.init(CONFIGOS)
    for name in NAMES:
        configos.load(name)
