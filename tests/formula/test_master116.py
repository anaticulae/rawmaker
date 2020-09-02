# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import rawmaker.math
import rawmaker.reader


def test_extract_math_master116_page22():
    source = power.MASTER116_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(22,))
    assert extracted
    content = utila.select_content(extracted, page=22)
    raw = raw_formula(content)
    # TODO: REMOVE (2.3) later
    expected = [
        '𝑇𝑇,𝑚𝑎𝑥=𝐹𝑍,𝑚𝑎𝑥·𝑟𝑅𝑎𝑑.(2.3)',
        '𝑇𝑇,𝑚𝑎𝑥≤𝑚𝑣𝑔𝜇𝑟𝑠·𝑟𝑅𝑎𝑑.(2.4)',
        '𝐹𝑍,𝑚𝑎𝑥=𝐹𝐺·𝜇𝑟𝑠.(2.2)',
        '𝐹𝐺=𝑚𝑣·𝑔,(2.1)',
    ]
    assert raw == expected


@pytest.mark.xfail(reason='support multiple formulas')
def test_extract_math_master116_page23_multiple_lines():
    source = power.MASTER116_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(23,))
    assert extracted
    content = utila.select_content(extracted, page=23)
    raw = raw_formula(content)
    expected = [
        '𝐹𝑊=𝐹𝐿+𝐹𝑅+𝐹𝑆𝑡+𝐹𝐴,(2.5)',
        '𝐹𝐿=0.5𝜌𝐿𝑐𝑤𝐴𝑣𝑣𝑟2,(2.6)',
        '𝜌𝐿=1,2041kg/m3.(2.7)',
        '𝑐𝑤(𝑛)={1,0 n=0, 1,3 n=1, 1,53+(𝑛−2)·0,14} 𝑛≥2.(2.8)',
    ]
    assert len(raw) == len(expected)


def raw_formula(formulas) -> list:
    return [''.join([char.value for char in formula]) for formula in formulas]
