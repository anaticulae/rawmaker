# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import rawmaker.math
import rawmaker.reader


def test_extract_math_master110_page28_48():
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


def test_extract_math_master110_page62_83():
    """Ensure to handle empty characters correctly. HINT: Don't know why
    empty characters are generated."""
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(62, 83))

    dumped = serializeraw.dump_rawformulas(extracted)
    # ensure that loading works correctly
    loaded = serializeraw.load_rawformulas(dumped)

    assert loaded == extracted


def test_extract_math_master110_page67():
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(67,))

    formulas = extracted[0].content
    assert len(formulas) == 3


def test_extract_math_master110_page59():
    source = power.MASTER110_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(59,))

    formulas = extracted[0].content
    assert len(formulas) == 7  # may change later
