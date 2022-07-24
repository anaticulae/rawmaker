#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import power
import serializeraw

import tests


def test_bachelor085_any_content(td, mp):
    """Remove single figure content container."""
    cmd = (f'-i {power.BACHELOR085_PDF} -o {td.tmpdir} --pages=0:5 --text '
           '--line --horizontal --images')
    tests.run(cmd, mp=mp)
    text = serializeraw.ptn_frompath(td.tmpdir)
    assert text
    horizontals = serializeraw.load_horizontals(td.tmpdir, width_min=10)
    assert horizontals
    images = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    assert images


def test_master116_any_content(td, mp):
    cmd = (f'-i {power.MASTER116_PDF} -o {td.tmpdir} --pages=0,1,2,3 --text '
           '--line --horizontal --images')
    tests.run(cmd, mp=mp)
    text = serializeraw.ptn_frompath(td.tmpdir)
    assert text
    horizontals = serializeraw.load_horizontals(td.tmpdir, width_min=10)
    assert horizontals
    images = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    assert images
