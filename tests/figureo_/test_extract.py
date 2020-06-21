# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import figureo.data
import figureo.extract
import tests.resources


def extract_figures(pages=None):
    """2 Figures on page 12 and 1 figure and 1 image on page 13."""
    source = tests.resources.MASTER116
    if pages is None:
        pages = (12, 13)
    extracted = figureo.extract.extract_figures(source, pages=pages)
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
        figureo.data.dump_figures(extracted, outpath)

    loaded = figureo.data.load_figures(outpath)
    assert len(loaded) == 3


def test_figures_extract_master116_page19(testdir):
    outpath = testdir.tmpdir
    extracted = extract_figures((19, 38))
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        figureo.data.dump_figures(extracted, outpath)
