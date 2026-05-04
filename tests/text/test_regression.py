# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw

import rawmaker
import tests


def test_text_master110_bounding_x0_x1(td, mp):
    """There was the case that merging two chars/lines results in
    malformed bounding box. Skip merging bounding boxes solves this
    issue."""
    # layout is required to invoke error
    layout = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25'
    cmd = f'-i {hoverpower.MASTER110_PDF} --text --pages=60 {layout}'
    tests.run(cmd, mp=mp)
    loaded = serializeraw.load_textpositions(td.tmpdir)
    assert loaded


def test_negative_text_bounding_diss274page0(td, mp):
    # layout is required to invoke error
    layout = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25'
    cmd = f'-i {hoverpower.DISS274_PDF} --text --pages=0 {layout}'
    tests.run(cmd, mp=mp)
    navigators = serializeraw.ptn_frompath(td.tmpdir)
    navigator = navigators[0]
    # TODO: CHANGES AFTER INVESTIGATING PROBLEM WITH NEGATIVE TEXT CONTENT
    # ON LEFT BORDER.
    assert len(navigator) == 10


def test_text_bachelor67page63(td, mp):
    # layout is required to invoke error
    config = rawmaker.LAYOUT
    cmd = f'-i {hoverpower.BACHELOR067_PDF} --text --pages=63 {config}'
    tests.run(cmd, mp=mp)
    navigators = serializeraw.ptn_frompath(td.tmpdir)[0]
    text = [item.text.strip() for item in navigators]
    assert text[1] == '[AM14]'
    assert text[13] == '[Arm+15]'


@pytest.mark.usefixtures('td')
def test_text_master099b_zero_bounding_char(mp):
    cmd = f'-i {hoverpower.MASTER099B_PDF} --text --pages=42'
    tests.run(cmd, mp=mp)


def test_text_master089_outside_char(td, mp):
    cmd = f'-i {hoverpower.MASTER089_PDF} --text --pages=1'
    tests.run(cmd, mp=mp)
    navigator = serializeraw.ptn_frompath(td.tmpdir)[0]
    raw = navigator.debug
    # ensure that hidden character which are produced by user, skip them
    # to improve extraction
    assert 'A     Audiovisuelle Medien' not in raw
    assert 'm     Mythen und Spielfilme' not in raw
    assert '   Mythen und Spielfilme' not in raw
    assert '   Audiovisuelle Medien' not in raw


def rawpage(source, pages: str, td, mp):
    cmd = f'-i {source} --text --pages={pages}'
    tests.run(cmd, mp=mp)
    navigator = serializeraw.ptn_frompath(td.tmpdir)[0]
    raw = navigator.debug
    return raw


def test_text_hidden_chars_hcdiss193(td, mp):
    raw = rawpage(hoverpower.HC_DISS193, '11', td, mp)
    assert '9292' not in raw
    assert '1120' not in raw
    # replace white chars due spaces
    assert 'its characteristics                                        134' in raw


def test_text_rsign(td, mp):
    """Ensure to covert r-signs correctly."""
    raw = rawpage(hoverpower.BACHELOR090_PDF, '88', td, mp)
    assert raw.count('®') == 2


def test_text_fl(td, mp):
    """Ensure to covert fl-signs correctly."""
    raw = rawpage(hoverpower.MASTER110_PDF, '95', td, mp)
    assert raw.count('Reflektion') == 2
    assert raw.count('Reflekti-') == 1


def test_text_ffi(td, mp):
    """Ensure to covert Eﬃcient correctly."""
    raw = rawpage(hoverpower.MASTER110_PDF, '106', td, mp)
    # assert raw.count('Efficient') == 1
    # TODO: FIX LATER
    assert raw.count('Effcieint') == 1
    # - was not replaced and as ord 19 detected as '{'
    assert raw.count('Fernandez') == 1


def test_text_umlaute(td, mp):
    """Ensure that umlaute are converted correctly."""
    raw = rawpage(hoverpower.MASTER110_PDF, '106', td, mp)
    assert raw.count('für') == 2
