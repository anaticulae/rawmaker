# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from utila import file_create
from yaml import FullLoader
from yaml import load

from rawmaker import read
from rawmaker.features.fonts import work
from tests.resource import DOCUMENTATION_TWINE_PDF
from tests.resource import INCREASING_FONT_A4


def test_mining_fonts(testdir):
    header, content = None, None
    with read(DOCUMENTATION_TWINE_PDF) as pdf:
        result = work(pdf)
        header, content = result['header'], result['content']

    assert len(header) > 100
    assert len(content) > 300

    file_create('header.yaml', header)
    file_create('content.yaml', content)


@mark.xfail()
def test_mining_increasing_fonts():
    # TODO: Investiga later
    with read(INCREASING_FONT_A4) as pdf:
        result = work(pdf)
        header, content = result['header'], result['content']

    for item in load(header, Loader=FullLoader):
        # print(item['font']['scale'])
        # print(round(item['font']['scale'] - 3.15))
        print('%0.0f' % (item['font']['scale'] - 3.1))
    assert 0
