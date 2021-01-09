# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import serializeraw

import tests


def test_diss272_formula_load(testdir, monkeypatch):
    """There was a problem in formula raw loader when formula is only
    one char long."""
    # TODO: REMOVE THIS TEST AFTER FIXING FORMULA PARSER
    # TODO: REMOVE UTILA PARSE_TUPLE PATCH LATER
    cmd = f'-i {power.DISS272_PDF} --formula --pages=201'
    tests.run(cmd, monkeypatch=monkeypatch)

    source = os.path.join(testdir.tmpdir, 'rawmaker__formula_formula.yaml')
    loaded = serializeraw.load_rawformulas(source)
    loaded = loaded[0].content
    assert len(loaded) > 10
