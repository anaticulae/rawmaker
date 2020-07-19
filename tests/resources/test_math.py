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

import rawmaker.math
import rawmaker.reader


def test_extract_math():
    source = power.HOMEWORK050_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(8,))

    formula = utila.select_content(extracted, page=8)
    assert len(formula) == 3
