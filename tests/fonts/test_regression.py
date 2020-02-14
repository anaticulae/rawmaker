# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import tests
import tests.resources


def test_leftright_book_font_size(testdir, monkeypatch):
    tests.run_success(
        f'-i {tests.resources.LEFTRIGHT} --text',
        monkeypatch=monkeypatch,
    )
    position = serializeraw.load_document('rawmaker__text_text.yaml')
    first_page = utila.select_page(position, page=0)
    first_char = first_page[0][0][0]
    # ensure that a higher font size than 1 is detected. There was/is a
    # bug with font size determination.
    assert first_char.size >= 8.0, first_char
