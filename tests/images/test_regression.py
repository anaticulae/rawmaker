# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw.images
import utila
import utilatest

import tests
import tests.resources


@utilatest.longrun
def test_image_extract_with_pages_offset(testdir, monkeypatch):
    """This test ensures that the image information is stored correctly
    even if only a part of --pages=10:20 is extracted."""
    cmd = f'-i {power.MASTER116_PDF} --images --pages=16:20'
    tests.run(cmd, monkeypatch=monkeypatch)

    images = serializeraw.images.load_image_informations_frompath(
        testdir.tmpdir)
    pages = {image.page for image in images}
    assert pages == {16, 17}, pages


@utilatest.longrun
def test_render_master75_page0_10_28(monkeypatch, testdir):
    """This document contains images on different pages with the same
    name. Before this fix, these images where ignored cause of the same
    name. After adding the page number to image name, these images are
    extracted correctly."""
    cmd = f'-i {power.MASTER075_PDF} --pages=0:10,28 --images'
    tests.run(cmd, monkeypatch=monkeypatch)
    written = utila.file_list('rawmaker__images_images')
    expected = 8
    assert len(written) == expected, str(written)

    # ensure to define pages correctly
    images = serializeraw.images.load_image_informations_frompath('.')
    content = [[item.page for item in page.content] for page in images]
    pages = utila.flatten(content)
    assert pages == [0, 8, 28, 28]


def test_render_master127page32(monkeypatch, testdir):
    """Ensure that multi-line-image is merged correctly."""
    cmd = f'-i {power.MASTER127_PDF} --pages=32 --images'
    tests.run(cmd, monkeypatch=monkeypatch)
    written = utila.file_list('rawmaker__images_images')
    expected = 2
    assert len(written) == expected, str(written)


def test_skip_huge_image(monkeypatch, testdir, capsys):
    """Skip image which is able to overload infrastructure cause it is
    very huge."""
    cmd = f'-i {tests.resources.IMAGE_HUGEMONO} --images -VVV'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert 'skip image size:' in utilatest.stdout(capsys)


def test_image_write_error(monkeypatch, testdir):
    cmd = f'-i {power.DISS143_PDF} --images --pages=85'
    tests.run(cmd, monkeypatch=monkeypatch)
    extracted = utila.file_list('rawmaker__images_images', include='png')
    assert len(extracted) == 1


def test_image_master31page10(monkeypatch, testdir):
    """Chinese character should be the only image."""
    cmd = f'-i {power.MASTER031_PDF} --images --pages=10'
    tests.run(cmd, monkeypatch=monkeypatch)
    extracted = utila.file_list('rawmaker__images_images', include='png')
    assert len(extracted) == 1
