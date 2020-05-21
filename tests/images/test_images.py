# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import rawmaker.miner.images
import rawmaker.reader
import tests
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


@pytest.mark.parametrize('page, expected, ext, expected_bounding_height', [
    (10, 1, 'png', 140),
    (19, 1, 'png', 291),
    (54, 1, 'png', 340),
    (54, 1, 'jpg', 340),
    (55, 1, 'png', 600),
    (56, 1, 'png', 600),
    (57, 1, 'png', 600),
])
def test_images_export_bachelor63_extract_images(
        page,
        expected,
        ext,
        expected_bounding_height,
        testdir,
):
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
    image = extracted[0][0]
    bounding = image.bounding
    height = bounding[3] - bounding[1]
    assert height >= expected_bounding_height, str(bounding)


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(
            tests.resources.BACHELOR111,
            999,
            id='bachelor111',
            marks=pytest.mark.xfail(reason='not fully supported'),
        ),
        # pytest.param(tests.resources.TWINE_PDF, 0, id='twine'),
        pytest.param(tests.resources.TECHNICAL24, 8, id='technical24'),
        pytest.param(tests.resources.REPORT19, 6, id='report19'),
    ])
@utila.skip_longrun
def test_images_export_document_complete(
        source,
        expected,
        testdir,
        monkeypatch,
):
    # for every image it is an additonal image info file extracted.
    root = testdir.tmpdir
    with utila.increased_filecount(root, mindiff=expected, maxdiff=expected):
        cmd = f'-i {source} --images'
        tests.run_success(cmd, monkeypatch=monkeypatch)
