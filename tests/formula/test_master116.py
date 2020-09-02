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


@pytest.mark.parametrize('page, expected', [
    (
        22,
        [
            '𝐹𝐺=𝑚𝑣·𝑔,(2.1)',
            '𝐹𝑍,𝑚𝑎𝑥=𝐹𝐺·𝜇𝑟𝑠.(2.2)',
            '𝑇𝑇,𝑚𝑎𝑥=𝐹𝑍,𝑚𝑎𝑥·𝑟𝑅𝑎𝑑.(2.3)',
            '𝑇𝑇,𝑚𝑎𝑥≤𝑚𝑣𝑔𝜇𝑟𝑠·𝑟𝑅𝑎𝑑.(2.4)',
        ],
    ),
    (
        24,
        [
            '𝐹𝑅=(𝑚𝑣+𝑚𝑧)·𝑔·𝑓𝑅·cos𝛼𝑆𝑡.(2.9)',
            '𝐹𝐺=(𝑚𝑣+𝑚𝑧)·𝑔,(2.10)',
            '𝐹𝑆𝑡=𝐹𝐺·sin𝛼𝑆𝑡.(2.11)',
            '𝐹𝐴=𝐹𝐴,𝑡𝑟𝑎𝑛𝑠+𝐹𝐴,𝑟𝑜𝑡.(2.12)',
        ],
    ),
    (
        25,
        [
            '𝐽𝑇𝑟𝑎𝑛𝑠=𝑟𝑅2𝑎𝑑·(𝑚𝑣+𝑚𝑧).(2.13)',
            '𝐽𝐺𝑒𝑠=𝐽𝑇𝑟𝑎𝑛𝑠+𝐽𝑅𝑜𝑡.(2.14)',
            '𝐹𝐴,𝑟𝑜𝑡=1/𝑟𝑅𝑎𝑑𝐽𝑅𝑜𝑡𝜔˙W,(2.15)',
            '𝐹𝐴,𝑡𝑟𝑎𝑛𝑠=1/𝑟𝑅𝑎𝑑𝐽𝑇𝑟𝑎𝑛𝑠𝜔˙W.(2.16)',
            '𝐹𝐴=1/𝑟𝑅𝑎𝑑(𝐽𝑅𝑜𝑡+𝐽𝑇𝑟𝑎𝑛𝑠).(2.17)',
            '𝐸𝑊=𝑥𝐹𝑊(𝑠)·𝑑𝑠(2.18)',
            '𝐸𝑊,𝑘𝑜𝑛𝑠=[𝐹𝑆𝑡(𝑠)+𝐹𝐴(𝑠)]·𝑑𝑠,(2.19)',
            '𝐸𝑊,𝑑𝑖𝑠𝑠=[𝐹𝐿(𝑠)+𝐹𝑅(𝑠)]·𝑑𝑠.(2.20)',
            '𝑃𝑊=𝐹𝑊(𝑣𝑥)𝑣𝑥,(2.21)',
            '=0.5𝜌𝐿𝑐𝑤𝐴𝑣𝑣𝑥3+𝑣𝑥[︂(𝑚𝑣+𝑚𝑧)𝑔𝑓𝑅cos𝛼𝑆𝑡+1]︂.(2.22)',
        ],
    ),
])
def test_extract_math_master116_page_x(page, expected):
    source = power.MASTER116_PDF
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=(page,))
    assert extracted
    content = utila.select_content(extracted, page=page)
    raw = raw_formula(content)
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
