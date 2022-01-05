# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import linero.features.table
import linero.table.horizontal


def extract_tables(source, page):
    ptn = serializeraw.ptn_frompath(
        source,
        pages=(page,),
    )[0]
    lines = serializeraw.load_lines(
        iamraw.path.line(source),
        pages=(page,),
    )
    lines = lines[0].content
    tables = linero.table.horizontal.cluster_page(ptn, lines)
    return tables


@utilatest.requires(power.BACHELOR090_PDF)
def test_table_bachelor90page76_extract_table():
    source = power.link(power.BACHELOR090_PDF)
    page = 76
    tables = extract_tables(source, page)
    assert len(tables) == 1


@pytest.mark.xfail(reason='layout parameter changed')
@utilatest.requires(power.BACHELOR090_PDF)
def test_table_bachelor90page77_extract_table():
    source = power.link(power.BACHELOR090_PDF)
    page = 77
    tables = extract_tables(source, page)
    assert len(tables) == 3
