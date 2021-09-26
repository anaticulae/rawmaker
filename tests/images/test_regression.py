# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import serializeraw.images
import utila
import utilatest

import tests
import tests.resources


def extract(source, pages, testdir, monkeypatch) -> list:
    cmd = f'-i {source} --images --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    if not os.path.exists(testdir.tmpdir.join('rawmaker__images_images')):
        return []
    extracted = utila.file_list('rawmaker__images_images', include='png')
    return extracted


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
    extracted = extract(power.MASTER075_PDF, '0:10,28', testdir, monkeypatch)
    expected = 4
    assert len(extracted) == expected, str(extracted)

    # ensure to define pages correctly
    images = serializeraw.images.load_image_informations_frompath('.')
    content = [[item.page for item in page.content] for page in images]
    pages = utila.flatten(content)
    assert pages == [0, 8, 28, 28]


def test_render_master127page32(monkeypatch, testdir):
    """Ensure that multi-line-image is merged correctly."""
    extracted = extract(power.MASTER127_PDF, 32, testdir, monkeypatch)
    assert len(extracted) == 1, str(extracted)


def test_skip_huge_image(monkeypatch, testdir, capsys):
    """Skip image which is able to overload infrastructure cause it is
    very huge."""
    cmd = f'-i {tests.resources.IMAGE_HUGEMONO} --images -VVV'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert 'skip image size:' in utilatest.stdout(capsys)


def test_image_write_error(monkeypatch, testdir):
    extracted = extract(power.DISS143_PDF, 85, testdir, monkeypatch)
    assert len(extracted) == 1


def test_image_master31page10(monkeypatch, testdir):
    """Chinese character should be the only image."""
    extracted = extract(power.MASTER031_PDF, 10, testdir, monkeypatch)
    assert len(extracted) == 1


def test_image_master31page4(monkeypatch, testdir):
    """Do not detect anything as image"""
    extracted = extract(power.MASTER031_PDF, 4, testdir, monkeypatch)
    assert not extracted
