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


@pytest.mark.usefixtures('td')
@pytest.mark.xfail(reason='incomplete font detection implementation')
@utilatest.longrun
def test_leftright_book_font_name(mp, capsys):
    tests.run(
        f'-i {power.BOOK007_PDF} --fonts',
        mp=mp,
    )
    stderr = utilatest.stderr(capsys)
    assert 'ERROR' not in stderr


@pytest.mark.usefixtures('td')
@pytest.mark.xfail(reason='support ROMA')
@utilatest.longrun
def test_bachelor90_fontname(mp, capsys):
    """\
    TODO: VERIFY WHAT ROMAN MEANS
    """
    tests.run(
        f'-i {power.BACHELOR090_PDF} --fonts --pages=1:20',
        mp=mp,
    )
    stderr = utilatest.stderr(capsys)
    assert 'ERROR' not in stderr


@utilatest.longrun
def test_leftright_book_font_size(td, mp):
    tests.run(
        f'-i {power.BOOK007_PDF} --text',
        mp=mp,
    )
    source = iamraw.path.text(td.tmpdir)
    position = serializeraw.load_document(source)
    first_page = utila.select_page(position, page=0)
    first_char = first_page[0][0][0]
    # ensure that a higher font size than 1 is detected. There was/is a
    # bug with font size determination.
    assert first_char.size >= 8.0, first_char


@utilatest.longrun
@pytest.mark.parametrize('strip', [True, False])
def test_porting_module_font_index(strip, td, mp):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = (f'-i {power.DOCU009_PDF} --fonts --text {nostrip}')
    tests.run(cmd, mp=mp)
    source = iamraw.path.fontcontent(td.tmpdir)
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
def test_regression_extract_text_and_fonts(pdf, strip, td, mp):
    """Hint: One white space is always at the end of a line. Without
    striping there can be more than one white space at the end of a
    line."""
    nostrip = '' if strip else '--nostrip'
    cmd = f'-i {pdf} --fonts {nostrip}'
    tests.run(cmd, mp=mp)
    source = iamraw.path.fontcontent(td.tmpdir)
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


@pytest.mark.usefixtures('td')
@utilatest.nightly
def test_arabic_fonts(mp):
    """Line starts with a VirtualChar which crashed bounding box
    computation."""
    # TODO: CHECK INFLUENCE OF RIGHT TO LEFT WRITING
    cmd = f'-i {power.DISS272_PDF} --fonts --pages=246:251'
    tests.run(cmd, mp=mp)


@pytest.mark.usefixtures('td')
@pytest.mark.xfail(reason='verify font size')
def test_font_size_huge_master193(mp):
    cmd = f'-i {power.MASTER193_PDF} --fonts --text --pages=2'
    tests.run(cmd, mp=mp)
    # TODO: INVESTIGATE FONT SIZE PROBLEM
    assert 0


def test_font_bold_bachelor067page59(td, mp):
    cmd = f'-i {power.BACHELOR067_PDF} --text --fonts  --pages=59'
    tests.run(cmd, mp=mp)
    fontstore = serializeraw.fs_frompath(td.tmpdir)
    ptcn = serializeraw.ptn_frompath(td.tmpdir)
    page59 = ptcn[0][0:5]
    firstline = page59[0].style.fontid
    assert fontstore[firstline].weight == iamraw.fonts.Weight.BOLD
    secondline = page59[1].style.fontid
    assert fontstore[secondline].weight == iamraw.fonts.Weight.BOLD
    thirdline = page59[2].style.fontid
    assert fontstore[thirdline].weight == iamraw.fonts.Weight.MEDIUM


def test_font_underline_bachelor28p16(td, mp):
    cmd = f'-i {power.BACHELOR028_PDF} --text --line --horizontals --pages=16'
    tests.run(cmd, mp=mp)
    ptcn = serializeraw.ptn_frompath(td.tmpdir)
    assert not ptcn[0][0].style.underlined
    assert not ptcn[0][1].style.underlined
    page28headline = ptcn[0][2]
    underlined = page28headline.style.underlined
    assert underlined
    assert not ptcn[0][3].style.underlined
    # ensure that footer line does not invoke any underlines
    assert all(not item.style.underlined for item in ptcn[0][3:])
