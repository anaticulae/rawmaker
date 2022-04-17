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
import utila
import utilatest

import tests


@pytest.mark.xfail(reason='incomplete font detection implementation')
@utilatest.longrun
def test_leftright_book_font_name(testdir, monkeypatch, capsys):
    tests.run(
        f'-i {power.BOOK007_PDF} --fonts',
        monkeypatch=monkeypatch,
    )
    stderr = utilatest.stderr(capsys)
    assert 'ERROR' not in stderr


@pytest.mark.xfail(reason='support ROMA')
@utilatest.longrun
def test_bachelor90_fontname(testdir, monkeypatch, capsys):
    """\
    TODO: VERIFY WHAT ROMAN MEANS
    """
    tests.run(
        f'-i {power.BACHELOR090_PDF} --fonts --pages=1:20',
        monkeypatch=monkeypatch,
    )
    stderr = utilatest.stderr(capsys)
    assert 'ERROR' not in stderr


@utilatest.longrun
def test_leftright_book_font_size(testdir, monkeypatch):
    tests.run(
        f'-i {power.BOOK007_PDF} --text',
        monkeypatch=monkeypatch,
    )
    source = iamraw.path.text(testdir.tmpdir)
    position = serializeraw.load_document(source)
    first_page = utila.select_page(position, page=0)
    first_char = first_page[0][0][0]
    # ensure that a higher font size than 1 is detected. There was/is a
    # bug with font size determination.
    assert first_char.size >= 8.0, first_char


@utilatest.longrun
@pytest.mark.parametrize('strip', [True, False])
def test_porting_module_font_index(strip, testdir, monkeypatch):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = (f'-i {power.DOCU009_PDF} --fonts --text {nostrip}')
    tests.run(cmd, monkeypatch=monkeypatch)
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
    pytest.param(power.MASTER072_PDF, True, id='master72_true'),
    pytest.param(power.MASTER072_PDF, False, id='master72_false'),
])
@utilatest.nightly
def test_regression_extract_text_and_fonts(pdf, strip, testdir, monkeypatch):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = f'-i {pdf} --fonts {nostrip}'
    tests.run(cmd, monkeypatch=monkeypatch)
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


@utilatest.nightly
def test_arabic_fonts(testdir, monkeypatch):
    """Line starts with a VirtualChar which crashed bounding box
    computation."""
    # TODO: CHECK INFLUENCE OF RIGHT TO LEFT WRITING
    cmd = f'-i {power.DISS272_PDF} --fonts --pages=246:251'
    tests.run(cmd, monkeypatch=monkeypatch)


@pytest.mark.xfail(reason='verify font size')
def test_font_size_huge_master193(testdir, monkeypatch):
    cmd = f'-i {power.MASTER193_PDF} --fonts --text --pages=2'
    tests.run(cmd, monkeypatch=monkeypatch)
    # TODO: INVESTIGATE FONT SIZE PROBLEM
    assert 0


def test_font_bold_bachelor067page59(testdir, monkeypatch):
    cmd = f'-i {power.BACHELOR067_PDF} --text --fonts  --pages=59'
    tests.run(cmd, monkeypatch=monkeypatch)
    fontstore = serializeraw.fs_frompath(testdir.tmpdir)
    ptcn = serializeraw.ptn_frompath(testdir.tmpdir)
    page59 = ptcn[0][0:5]
    firstline = page59[0].style.fontid
    assert fontstore[firstline].weight == iamraw.fonts.Weight.BOLD
    secondline = page59[1].style.fontid
    assert fontstore[secondline].weight == iamraw.fonts.Weight.BOLD
    thirdline = page59[2].style.fontid
    assert fontstore[thirdline].weight == iamraw.fonts.Weight.MEDIUM


def test_font_underline_bachelor28p16(testdir, monkeypatch):
    cmd = f'-i {power.BACHELOR028_PDF} --text --line --horizontals --pages=16'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptcn = serializeraw.ptn_frompath(testdir.tmpdir)
    assert not ptcn[0][0].style.underlined
    assert not ptcn[0][1].style.underlined
    page28headline = ptcn[0][2]
    underlined = page28headline.style.underlined
    assert underlined
    assert not ptcn[0][3].style.underlined
    # ensure that footer line does not invoke any underlines
    assert all(not item.style.underlined for item in ptcn[0][3:])
