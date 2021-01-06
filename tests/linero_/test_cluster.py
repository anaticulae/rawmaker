# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw

import linero.features.table
import linero.table.horizontal


def extract_tables(source, page):
    ptn = serializeraw.create_pagetextnavigators_frompath(
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


def test_table_bachelor90_page76_extract_table():
    source = power.link(power.BACHELOR090_PDF)
    page = 76

    tables = extract_tables(source, page)
    assert len(tables) == 1


def test_table_bachelor90_page77_extract_table():
    source = power.link(power.BACHELOR090_PDF)
    page = 77

    tables = extract_tables(source, page)
    assert len(tables) == 3
