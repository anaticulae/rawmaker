# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import pytest
import utila

import rawmaker.miner.images
import rawmaker.reader
import tests.resources


@utila.skip_longrun
def test_images_export_bachelor56(testdir):
    """Extract seven images out of four pages."""
    source = tests.resources.BACHELOR56
    root = testdir.tmpdir
    pages = None
    with utila.increased_filecount(root, mindiff=7, maxdiff=7):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    four_image_pages = 4
    assert len(extracted) == four_image_pages, str(extracted)


@utila.skip_longrun
def test_images_export_bachelor63_complete(testdir):
    """Extract seven images out of four pages."""
    source = tests.resources.BACHELOR63
    root = testdir.tmpdir
    pages = None
    with utila.increased_filecount(root, mindiff=41, maxdiff=41):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert extracted


@utila.skip_nightly
def test_images_export_master116(testdir):
    source = tests.resources.MASTER116
    root = testdir.tmpdir
    pages = None
    # master116 contains **9** extractable images, but on page 50 the png
    # extraction is broken. After fix this issue we have to increase
    # number of extracted images.
    with utila.increased_filecount(root, mindiff=8, maxdiff=8):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert extracted


@pytest.mark.parametrize('page, expected, ext', [
    (10, 1, 'png'),
    (19, 1, 'png'),
    (54, 1, 'png'),
    (54, 1, 'jpg'),
    (55, 1, 'png'),
    (56, 1, 'png'),
    (57, 1, 'png'),
])
def test_images_export_bachelor63_merge_image(page, expected, ext, testdir):
    source = tests.resources.BACHELOR63
    root = testdir.tmpdir
    pages = (page,)
    with utila.increased_filecount(
            root,
            ext=ext,
            mindiff=expected,
            maxdiff=expected,
    ):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert extracted
