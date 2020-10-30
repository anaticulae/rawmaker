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
import serializeraw
import utila

import rawmaker.math
import rawmaker.reader
import tests


def test_extract_math_homework50_page8():
    source = power.HOME050_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(8,))

    formula = utila.select_content(extracted, page=8)
    assert len(formula) == 3


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
