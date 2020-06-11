# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import rawmaker.features.images
import rawmaker.images.info
import rawmaker.miner.images
import rawmaker.reader
import tests.resources


def test_image_information(testdir):
    """Extract image information for one image on first page of
    Bachelor56 example."""
    root = testdir.tmpdir
    source = tests.resources.BACHELOR56
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.miner.images.extract_images(
            pdf,
            outputfolder=root,
            pages=(0,),
        )
    pageone_firstimage = extracted[0][0]
    assert len(extracted) == 1
    path = os.path.join(root, pageone_firstimage.filename)
    info = rawmaker.images.info.imageinfo(
        path,
        page=0,
        bounding=pageone_firstimage.bounding,
    )
    assert info, info
    assert info.width >= 500, str(info)
    assert info.height >= 200, str(info)
