# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import rawmaker.path
import tests
import tests.resources


@pytest.mark.xfail(reason='incomplete font detection implementation')
def test_leftright_book_font_name(testdir, monkeypatch, capsys):
    tests.run_success(
        f'-i {tests.resources.LEFTRIGHT} --fonts',
        monkeypatch=monkeypatch,
    )
    _, err = capsys.readouterr()
    assert 'ERROR' not in err


def test_leftright_book_font_size(testdir, monkeypatch):
    tests.run_success(
        f'-i {tests.resources.LEFTRIGHT} --text',
        monkeypatch=monkeypatch,
    )
    source = rawmaker.path.text(testdir.tmpdir)
    position = serializeraw.load_document(source)
    first_page = utila.select_page(position, page=0)
    first_char = first_page[0][0][0]
    # ensure that a higher font size than 1 is detected. There was/is a
    # bug with font size determination.
    assert first_char.size >= 8.0, first_char


# @pytest.mark.xfail(reason='font parsing error')
def test_porting_module_font_index(testdir, monkeypatch):
    tests.run_success(
        f'-i {tests.resources.HOW_TO_CPORTING_PDF} --fonts --pages=0',
        monkeypatch=monkeypatch,
    )
    source = rawmaker.path.fontcontent(testdir.tmpdir)
    position = serializeraw.load_font_content(source)
    first_page = utila.select_page(position, page=0)[0]

    before_last = first_page[-2][0:3]
    last = first_page[-1][0:3]

    assert before_last != last, ('font extraction error, 2 different '
                                 'location can not be equal'
                                 f'{before_last} {last}')
