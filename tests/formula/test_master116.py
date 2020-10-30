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
import utilatest

import rawmaker.math
import rawmaker.reader


@pytest.mark.parametrize('page, expected', [
    (
        22,
        [
            '𝐹𝐺=𝑚𝑣·𝑔,',
            '𝐹𝑍,𝑚𝑎𝑥=𝐹𝐺·𝜇𝑟𝑠.',
            '𝑇𝑇,𝑚𝑎𝑥=𝐹𝑍,𝑚𝑎𝑥·𝑟𝑅𝑎𝑑.',
            '𝑇𝑇,𝑚𝑎𝑥≤𝑚𝑣𝑔𝜇𝑟𝑠·𝑟𝑅𝑎𝑑.',
        ],
    ),
    (
        24,
        [
            '𝐹𝑅=(𝑚𝑣+𝑚𝑧)·𝑔·𝑓𝑅·cos𝛼𝑆𝑡.',
            '𝐹𝐺=(𝑚𝑣+𝑚𝑧)·𝑔,',
            '𝐹𝑆𝑡=𝐹𝐺·sin𝛼𝑆𝑡.',
            '𝐹𝐴=𝐹𝐴,𝑡𝑟𝑎𝑛𝑠+𝐹𝐴,𝑟𝑜𝑡.',
        ],
    ),
    pytest.param(
        25,
        [
            '𝐽𝑇𝑟𝑎𝑛𝑠=𝑟𝑅2𝑎𝑑·(𝑚𝑣+𝑚𝑧).',
            '𝐽𝐺𝑒𝑠=𝐽𝑇𝑟𝑎𝑛𝑠+𝐽𝑅𝑜𝑡.',
            '((22..1156))',
            '𝐹𝐴𝐹,𝑡𝐴𝑟,𝑎𝑟𝑛𝑜𝑠𝑡==11//𝑟𝑟𝑅𝑅𝑎𝑎𝑑𝑑𝐽𝐽𝑅𝑇𝑟𝑜𝑎𝑡𝑛𝜔˙𝑠W𝜔˙W,.',
            '𝐹𝐴=1/𝑟𝑅𝑎𝑑(𝐽𝑅𝑜𝑡+𝐽𝑇𝑟𝑎𝑛𝑠).',
            '𝐸𝑊=𝑥𝐹𝑊(𝑠)·𝑑𝑠',
            '𝐸𝑊,𝑘𝑜𝑛𝑠=[𝐹𝑆𝑡(𝑠)+𝐹𝐴(𝑠)]·𝑑𝑠,',
            '𝐸𝑊,𝑑𝑖𝑠𝑠=[𝐹𝐿(𝑠)+𝐹𝑅(𝑠)]·𝑑𝑠.',
            '𝑃𝑊==𝐹0.𝑊5𝜌(𝐿𝑣𝑐𝑥𝑤)𝑣𝐴𝑥𝑣,𝑣𝑥3+𝑣𝑥︂[(𝑚𝑣+𝑚𝑧)𝑔𝑓𝑅cos𝛼𝑆𝑡+𝑟𝑅1𝑎𝑑𝐽𝐺𝑒𝑠︂].((22..2212))',
        ],
        marks=pytest.mark.xfail(reason='changes often'),
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


@utilatest.skip_longrun
def test_extract_math_master116_zero_math():
    source = power.MASTER116_PDF
    pages = utila.ranged_tuple(0, 22)
    with rawmaker.reader.read(source) as pdf:
        extracted = rawmaker.math.extract_content(pdf, pages=pages)
    assert not extracted
