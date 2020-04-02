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


@contextlib.contextmanager
def increased_filecount(
        path: str,
        ext: str = None,
        mindiff: int = None,
        maxdiff: int = None,
):
    # TODO: REMOVE AFTER PATCHING UTILA
    """Ensure that some files were created while yielded operation.

    Args:
        path(str): path to check for file creation
        ext(str): look for a special file extention
        mindiff(int): minimal number of created files, if None 1 is used
        maxdiff(int): maximal number of created files, if None utila.INF is used
    Raises:
        AssertionError: if to few or less files are created
    Yields:
        None: to run file creation operation
    """
    import os
    import glob
    assert os.path.exists(path), str(path)
    assert mindiff is None or mindiff, str(mindiff)
    assert maxdiff is None or maxdiff, str(maxdiff)
    pattern = '**/*.*' if ext is None else f'**/*.{ext}'
    with utila.chdir(path):
        before = list(glob.glob(pattern, recursive=True))
        yield
        after = list(glob.glob(pattern, recursive=True))
    mindiff = 1 if mindiff is None else mindiff
    maxdiff = utila.INF if maxdiff is None else maxdiff
    current = len(after) - len(before)
    assert mindiff <= current <= maxdiff, (
        f'mindiff: {mindiff} maxdiff: {maxdiff}\n'
        '{before}\n\n{after}')


utila.increased_filecount = increased_filecount


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
