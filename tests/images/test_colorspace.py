# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import rawmaker.miner.images
import tests


def test_reg_image_colorspace_four_items(td):
    """First page with colorspace:

    [/'Indexed', /'DeviceRGB', 255, <PDFObjRef:16>] on page zero.
    """
    with rawmaker.reader.read(hoverpower.MASTER091A_PDF) as pdf:
        extracted = rawmaker.miner.images.extract_images(
            pdf,
            outputfolder=td.tmpdir,
            pages=(0,),
        )
    assert len(extracted) == 1


@tests.ghost
@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.ORDER044_PDF, id='order44'),
    pytest.param((hoverpower.MASTER083_PDF, '83'), id='master83'),
])
@utilotest.longrun
def test_reg_images_colorspace(source, mp):
    try:
        source, page = source
    except ValueError:
        page = ':'
    cmd = f'-i {source} --images --pages={page}'
    tests.run(cmd, mp=mp)
