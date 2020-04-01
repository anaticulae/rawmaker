# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import rawmaker.miner.images
import rawmaker.reader
import tests.resources


def test_images_export_bachelor56(testdir):
    """Extract seven images out of four pages."""
    source = tests.resources.BACHELOR56
    root = testdir.tmpdir
    pages = None
    with utila.increased_filecount(root, diff=7):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert len(extracted) == 4, str(extracted)


def test_images_export_bachelor63(testdir):
    """Extract seven images out of four pages."""
    source = tests.resources.BACHELOR63
    root = testdir.tmpdir
    pages = None
    with utila.increased_filecount(root, diff=32):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert extracted
