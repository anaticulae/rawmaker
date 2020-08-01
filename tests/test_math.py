# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import rawmaker.features.formula
import rawmaker.math
import rawmaker.path
import rawmaker.reader
import tests


def test_extract_math():
    source = power.HOMEWORK050_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(8,))

    formula = utila.select_content(extracted, page=8)
    assert len(formula) == 3


def test_extract_math_master116_zero_math():
    source = power.MASTER116_PDF
    pages = utila.ranged_tuple(0, 22)
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=pages)
    assert not extracted


def test_extract_math_master116_page22_23():
    source = power.MASTER116_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(22, 23))
    assert extracted
    content = utila.select_content(extracted, page=22)
    assert len(content) == 4

    content = utila.select_content(extracted, page=23)
    assert len(content) == 4


def test_dump_and_load_formula(testdir, monkeypatch):
    source = power.BACHELOR090_PDF

    tests.run(f'-i {source} --formula --pages=51', monkeypatch=monkeypatch)

    formula = rawmaker.path.formula(testdir.tmpdir)
    loaded = rawmaker.features.formula.load_rawformulas(formula)
    assert loaded
    assert len(loaded[0].content) == 1
    dumped = rawmaker.features.formula.dump_rawformulas(loaded)

    loadafter = rawmaker.features.formula.load_rawformulas(dumped)
    assert loadafter == loaded
