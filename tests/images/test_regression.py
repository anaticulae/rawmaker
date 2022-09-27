# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw.images
import utila
import utilatest

import tests
import tests.resources


def extract(source, pages, td, mp) -> list:
    cmd = f'-i {source} --images --pages={pages}'
    tests.run(cmd, mp=mp)
    if not os.path.exists(td.tmpdir.join('rawmaker__images_images')):
        return []
    extracted = utila.file_list('rawmaker__images_images', include='png')
    return extracted


@tests.ghost
@utilatest.longrun
def test_image_extract_with_pages_offset(td, mp):
    """This test ensures that the image information is stored correctly
    even if only a part of --pages=10:20 is extracted."""
    cmd = f'-i {power.MASTER116_PDF} --images --pages=16:20'
    tests.run(cmd, mp=mp)
    images = serializeraw.images.load_image_informations_frompath(td.tmpdir)
    pages = {image.page for image in images}
    assert pages == {16, 17}, pages


@tests.ghost
@utilatest.longrun
def test_render_master75page0_10_28(mp, td):
    """This document contains images on different pages with the same
    name. Before this fix, these images where ignored cause of the same
    name. After adding the page number to image name, these images are
    extracted correctly."""
    extracted = extract(power.MASTER075_PDF, '0:10,28', td, mp)
    expected = 4
    assert len(extracted) == expected, str(extracted)

    # ensure to define pages correctly
    images = serializeraw.images.load_image_informations_frompath('.')
    content = [[item.page for item in page.content] for page in images]
    pages = utila.flatten(content)
    assert pages == [0, 8, 28, 28]


@tests.ghost
@utilatest.longrun
def test_render_master127page32(mp, td):
    """Ensure that multi-line-image is merged correctly."""
    extracted = extract(power.MASTER127_PDF, 32, td, mp)
    assert len(extracted) == 1, str(extracted)


@tests.ghost
@pytest.mark.usefixtures('testdir')
def test_skip_huge_image(mp, capsys):
    """Skip image which is able to overload infrastructure cause it is
    very huge."""
    cmd = f'-i {tests.resources.IMAGE_HUGEMONO} --images -VVV'
    tests.run(cmd, mp=mp)
    assert 'skip image size:' in utilatest.stdout(capsys)


@tests.ghost
@utilatest.longrun
def test_image_write_error(mp, td):
    extracted = extract(power.DISS143_PDF, 85, td, mp)
    assert len(extracted) == 1


@tests.ghost
@utilatest.longrun
def test_image_master31page10(mp, td):
    """Chinese character should be the only image."""
    extracted = extract(power.MASTER031_PDF, 10, td, mp)
    assert len(extracted) == 1


def test_image_master31page4(mp, td):
    """Do not detect anything as image"""
    extracted = extract(power.MASTER031_PDF, 4, td, mp)
    assert not extracted


@pytest.mark.skip(reason='investigate bounding behavior')
def test_image_master105(mp, td):
    # extracted = extract(power.MASTER105_PDF, '89,90,91', td, mp)
    path = os.path.join(power.generated('shorten'), 'master105.pdf')
    extracted = extract(path, ':', td, mp)
    assert not extracted
