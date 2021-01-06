# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import rawmaker.miner.images
import rawmaker.reader
import tests


@utilatest.skip_longrun
def test_images_export_bachelor56(testdir):
    """Extract seven images out of four pages."""
    source = power.BACHELOR056_PDF
    root = testdir.tmpdir
    pages = None
    with utilatest.increased_filecount(root, mindiff=7, maxdiff=7):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    four_image_pages = 4
    assert len(extracted) == four_image_pages, str(extracted)


@utilatest.skip_nightly
def test_images_export_bachelor63_complete(testdir):
    """Extract seven images out of four pages."""
    source = power.BACHELOR063_PDF
    root = testdir.tmpdir
    pages = None
    with utilatest.increased_filecount(root, mindiff=41, maxdiff=41):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    assert extracted


@utilatest.skip_nightly
def test_images_export_master116(testdir):
    source = power.MASTER116_PDF
    root = testdir.tmpdir
    pages = None
    # master116 contains **9** extractable images, but on page 50 the png
    # extraction is broken. After fix this issue we have to increase
    # number of extracted images.
    with utilatest.increased_filecount(root, mindiff=8, maxdiff=8):
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
@utilatest.skip_longrun
def test_images_export_bachelor63_extract_images(
        page,
        expected,
        ext,
        expected_bounding_height,
        testdir,
):
    source = power.BACHELOR063_PDF
    root = testdir.tmpdir
    pages = (page,)
    with utilatest.increased_filecount(
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
    image = extracted[page][0]
    bounding = image.bounding
    height = bounding[3] - bounding[1]
    assert height >= expected_bounding_height, str(bounding)


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(
            power.BACHELOR111_PDF,
            999,
            id='bachelor111',
            marks=pytest.mark.xfail(reason='not fully supported'),
        ),
        # pytest.param(power.DOCU35_PDF, 0, id='twine'),
        pytest.param(power.TECH024_PDF, 8, id='technical24'),
        # pytest.param(tests.resources.REPORT19, 6, id='report19'),
        pytest.param(power.PAPER18_PDF, 10, id='paper18'),
    ])
@utilatest.skip_nightly
def test_images_export_document_complete(
        source,
        expected,
        testdir,
        monkeypatch,
):
    # for every image an additonal image info file is extracted.
    root = testdir.tmpdir
    with utilatest.increased_filecount(
            root,
            mindiff=expected,
            maxdiff=expected,
    ):
        cmd = f'-i {source} --images'
        tests.run(cmd, monkeypatch=monkeypatch)
