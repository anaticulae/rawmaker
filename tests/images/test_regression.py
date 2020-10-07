# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw.images

import tests


def test_image_extract_with_pages_offset(testdir, monkeypatch):
    """This test ensures that the image information is stored correctly
    even if only a part of --pages=10:20 is extracted."""
    cmd = f'-i {power.MASTER116_PDF} --images --pages=16:20'
    tests.run(cmd, monkeypatch=monkeypatch)

    images = serializeraw.images.load_image_informations_frompath(
        testdir.tmpdir)
    pages = {image.page for image in images}
    assert pages == {16, 17}, pages
