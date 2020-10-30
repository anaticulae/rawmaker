# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker.math
import rawmaker.reader
import tests


def test_extract_math_homework50_page8():
    source = power.HOME050_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(8,))

    formula = utila.select_content(extracted, page=8)
    assert len(formula) == 3


@utilatest.skip_longrun
def test_extract_math_master116_zero_math():
    source = power.MASTER116_PDF
    pages = utila.ranged_tuple(0, 22)
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=pages)
    assert not extracted


def test_dump_and_load_formula(testdir, monkeypatch):
    source = power.BACHELOR090_PDF
    tests.run(f'-i {source} --formula --pages=51', monkeypatch=monkeypatch)

    formula = iamraw.path.formula(testdir.tmpdir)
    loaded = serializeraw.load_rawformulas(formula)
    assert loaded
    assert len(loaded[0].content) == 1
    dumped = serializeraw.dump_rawformulas(loaded)

    loadafter = serializeraw.load_rawformulas(dumped)
    assert loadafter == loaded


@pytest.mark.xfail(reason='extend supported character of font parser')
def test_extract_math_master110():
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(28, 48))

    page28 = utila.select_content(extracted, page=28)
    assert len(page28) == 1
    page48 = utila.select_content(extracted, page=48)
    assert len(page48) == 3


def test_extract_math_master110_page29():
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(29,))

    page29 = utila.select_content(extracted, page=29)
    assert len(page29) == 2
    assert page29[0].page == 29
    assert page29[1].page == 29


def test_extract_math_master110_page62():
    """Ensure to handle empty characters correctly. HINT: Don't know why
    empty characters are generated."""
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(62,))

    dumped = serializeraw.dump_rawformulas(extracted)
    # ensure that loading works correctly
    loaded = serializeraw.load_rawformulas(dumped)

    assert loaded == extracted
