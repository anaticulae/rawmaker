# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import pytest
import serializeraw
import utila

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


@utila.skip_longrun
def test_leftright_book_font_size(testdir, monkeypatch):
    tests.run_success(
        f'-i {tests.resources.LEFTRIGHT} --text',
        monkeypatch=monkeypatch,
    )
    source = iamraw.path.text(testdir.tmpdir)
    position = serializeraw.load_document(source)
    first_page = utila.select_page(position, page=0)
    first_char = first_page[0][0][0]
    # ensure that a higher font size than 1 is detected. There was/is a
    # bug with font size determination.
    assert first_char.size >= 8.0, first_char


@pytest.mark.parametrize('strip', [True, False])
def test_porting_module_font_index(strip, testdir, monkeypatch):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = (f'-i {tests.resources.HOW_TO_CPORTING_PDF}'
           f' --fonts --text {nostrip}')
    tests.run_success(cmd, monkeypatch=monkeypatch)
    source = iamraw.path.fontcontent(testdir.tmpdir)
    position = serializeraw.load_font_content(source)

    for page in position:
        content = page.content
        if len(content) < 2:
            # not enough data on page
            continue
        before_last = content[-2][0:3]
        last = content[-1][0:3]
        assert before_last != last, ('font extraction error, 2 different '
                                     'location can not be equal'
                                     f'{before_last} {last}')


@pytest.mark.parametrize('pdf, strip', [
    pytest.param(tests.resources.MASTER72, True, id='master72_true'),
    pytest.param(tests.resources.MASTER72, False, id='master72_false'),
])
@utila.skip_longrun
def test_regression_extract_text_and_fonts(pdf, strip, testdir, monkeypatch):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = f'-i {pdf} --fonts {nostrip}'
    tests.run_success(cmd, monkeypatch=monkeypatch)
    source = iamraw.path.fontcontent(testdir.tmpdir)
    position = serializeraw.load_font_content(source)
    for page in position:
        content = page.content
        if len(content) < 2:
            # not enough data on page
            continue
        before_last = content[-2][0:3]
        last = content[-1][0:3]
        assert before_last != last, ('font extraction error, 2 different '
                                     'location can not be equal '
                                     f'page: {page.page} '
                                     f'position: {before_last} {last}')

    for index, page in enumerate([page.content for page in position]):
        items = [item[0:3] for item in page]
        assert all(item != (0, 0, 0) for item in items), f'{index} | {items}'
