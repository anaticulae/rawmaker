# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import rawmaker.miner.images


def test_reg_image_colorspace_four_items(testdir):
    """First page with colorspace:

    [/'Indexed', /'DeviceRGB', 255, <PDFObjRef:16>] on page zero.
    """
    with rawmaker.reader.read(power.MASTER091A_PDF) as pdf:
        extracted = rawmaker.miner.images.extract_images(
            pdf,
            outputfolder=testdir.tmpdir,
            pages=(0,),
        )
    assert len(extracted) == 1
