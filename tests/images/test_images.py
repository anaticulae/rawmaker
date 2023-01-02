# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hardcore
import power
import pytest
import utila
import utilatest

import rawmaker.miner.images
import rawmaker.reader
import tests


@utilatest.nightly
def test_images_export_bachelor56(td):
    """Extract seven images out of four pages."""
    source = power.BACHELOR056_PDF
    root = td.tmpdir
    pages = None
    expected = 5  # NOT VALIDATED
    with utilatest.increased_filecount(
            root,
            mindiff=expected,
            maxdiff=expected,
    ):
        with rawmaker.reader.read(source) as pdf:
            extracted = rawmaker.miner.images.extract_images(
                pdf,
                root,
                pages=pages,
            )
    four_image_pages = 4
    assert len(extracted) == four_image_pages, str(extracted)


@utilatest.nightly
def test_images_export_bachelor63_complete(td):
    """Extract seven images out of four pages."""
    source = power.BACHELOR063_PDF
    root = td.tmpdir
    pages = None
    expected = 41  # NOT VALIDATED
    with utilatest.increased_filecount(
            root,
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


@utilatest.nightly
def test_images_export_master116(td):
    source = power.MASTER116_PDF
    root = td.tmpdir
    pages = None
    # master116 contains **9?** extractable images, but on page 50 the png
    # extraction is broken. After fix this issue we have to increase
    # number of extracted images.
    expected = 11  # VALIDATED?
    with utilatest.increased_filecount(
            root,
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


@pytest.mark.parametrize('page, expected, ext, expected_bounding_height', [
    (10, 1, 'png', 140),
    (19, 1, 'png', 291),
    (54, 1, 'png', 340),
    (54, 1, 'jpg', 340),
    (55, 1, 'png', 600),
    (56, 1, 'png', 600),
    (57, 1, 'png', 600),
])
@utilatest.longrun
def test_images_export_bachelor63_extract_images(
    page,
    expected,
    ext,
    expected_bounding_height,
    td,
):
    source = power.BACHELOR063_PDF
    root = td.tmpdir
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


@tests.ghost
@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(
            power.BACHELOR111_PDF,
            999,
            id='bachelor111',
            marks=pytest.mark.xfail(reason='not fully supported'),
        ),
        # pytest.param(power.DOCU035_PDF, 0, id='twine'),
        # pytest.param(power.TECH024_PDF, 8, id='technical24'),
        pytest.param(power.TECH024_PDF, 6, id='technical24'),
        # pytest.param(tests.resources.REPORT19, 6, id='report19'),
        pytest.param(power.PAPER18_PDF, 12, id='paper18'),  # NOT VALIDATED
    ])
@utilatest.nightly
def test_images_export_document_complete(source, expected, td, mp):
    # for every image an additional image info file is extracted.
    root = td.tmpdir
    with utilatest.increased_filecount(
            root,
            mindiff=expected,
            maxdiff=expected,
    ):
        cmd = f'-i {source} --images'
        tests.run(cmd, mp=mp)


# TODO: INVESTIGATE PAGE WRITING ERROR ON PAGE 51. DON'T KNOW WHY FILE
# WRITING DOES NOT FAIL IF ONLY SINGLE PAGE IS SELECTED AND WHY NOT IF
# MORE THAN ONE IS SELECTED
AUDACITY = hardcore.single('audacity')


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR063_PDF, 12, 1, id='bachelor063'),
    pytest.param(power.BACHELOR090_PDF, (18, 58), 2, id='bachelor90'),
    pytest.param(power.DISS218_PDF, 24, 1, id='diss218JPXregression'),
    pytest.param(power.DISS218_PDF, 43, 1, id='diss218BitmapRegression'),
    pytest.param(power.DISS233_PDF, 61, 1, id='diss233'),
    pytest.param(power.MASTER099_PDF, 21, 1, id='master099'),
    pytest.param(power.MASTER105_PDF, 34, 1, id='master105'),
    pytest.param(power.MASTER116_PDF, (2, 3), 2, id='master116'),
    pytest.param(AUDACITY, utila.rtuple(40, 100), 101, id='audacity'),
])
def test_images_export_x(source, pages, expected, td):
    root = td.tmpdir
    with rawmaker.reader.read(source) as pdf:
        rawmaker.miner.images.extract_images(
            pdf,
            root,
            pages=pages,
        )
    extracted = utila.file_list(
        root,
        absolute=True,
    )
    assert len(extracted) == expected
