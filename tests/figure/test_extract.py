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
import utilatest

import rawmaker.features.figures
import rawmaker.figure.data
import tests
import tests.resources


def extract_figures(pages=None):
    """2 Figures on page 12 and 1 figure and 1 image on page 13."""
    source = tests.resources.MASTER116
    if pages is None:
        pages = (12, 13)
    extracted = rawmaker.features.figures.work(source, pages=pages)
    assert extracted
    return extracted


def test_figures_extract():
    extracted = extract_figures()
    assert len(extracted) == 3, str(extracted)


def test_figures_dump_and_load(testdir):
    outpath = testdir.tmpdir
    extracted = extract_figures()
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        rawmaker.figure.data.dump_figures(extracted, outpath)

    loaded = rawmaker.figure.data.load_figures(outpath)
    assert len(loaded) == 3


def test_figures_extract_master116_page19(testdir):
    outpath = testdir.tmpdir
    extracted = extract_figures((19, 38))
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        rawmaker.figure.data.dump_figures(extracted, outpath)


@pytest.mark.usefixtures('testdir')
def test_figures_run_master116(monkeypatch):
    source = tests.resources.MASTER116
    cmd = f'-i {source} --pages=17:24 --figures'
    tests.run(cmd, monkeypatch=monkeypatch)

    expected_file_count = 7 * 2
    written = utila.file_list('rawmaker__figures_figures')
    assert len(written) == expected_file_count, str(written)
