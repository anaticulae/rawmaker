#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import iamraw
import power
import pytest
import serializeraw
import utilatest

import rawmaker.features
import rawmaker.features.text
import tests.resources


@utilatest.longrun
def test_miner_pdf():
    parsed_file = rawmaker.features.text.work(power.DOCU013_PDF)
    assert parsed_file


def test_mine_hello_world_pdf():
    text, _ = rawmaker.features.text.work(tests.resources.HELLO_WORLD_PDF)
    loaded = serializeraw.load_document(text)

    assert loaded
    assert len(loaded) == tests.resources.HELLO_WORLD_PAGES


@pytest.mark.parametrize(
    'pdf_path',
    [
        tests.resources.HELLO_WORLD_PDF,
        power.DOCU013_PDF,
    ],
    ids=[
        'hello_world.pdf',
        'vimguide.pdf',
    ],
)
@utilatest.longrun
def test_dump_and_load_pdf(pdf_path):
    """Parse text from pdf file and write the result. Load the result after
    and compare with item to save"""
    text = rawmaker.features.text.extract_document(pdf_path)
    assert text
    dumped = serializeraw.dump_document(text)
    loaded = serializeraw.load_document(dumped)
    # Saving document saves only data not the bounding. The bounding is
    # stored in an other class. Therefore we have to ensure that
    # BoudingBox'es are equal before we compare the content.
    # NOTE: IN THIS CASE WE COMPARE ONLY THE TEXT CONTENT
    assert len(loaded) == len(text)
    for pageloaded, pageexpected in zip(loaded, text):
        for itemloaded, itemexpected in zip(pageloaded, pageexpected):
            # itemloaded.box = itemexpected.box
            if not isinstance(itemloaded, iamraw.TextContainer):
                continue

            for line, lineexpe in zip(itemloaded.lines, itemexpected.lines):
                assert line.text == lineexpe.text


def test_text_mine_pdf_page_0():
    selected_pages = [3, 4, 5]
    parsed = rawmaker.features.text.work(
        power.DOCU013_PDF,
        pages=selected_pages,
    )
    dumped_text, _ = parsed
    text = serializeraw.load_document(dumped_text)
    assert len(text) == len(selected_pages)
    text_page_numbers = [item.page for item in text]
    assert text_page_numbers == selected_pages, str(text_page_numbers)


@pytest.mark.parametrize('remove_whitespace', [True, False])
def test_text_mine_bachelor37_holy_whitespaces_remove(remove_whitespace):
    source = power.BACHELOR037_PDF
    pages = (1,)
    mine_holywhitespace(source, remove_whitespace, pages, 1)


def validate_master116(firstpage):
    lastline = firstpage[-1].text
    assert lastline == 'Berlin, 19. April 2016\n', lastline


@pytest.mark.parametrize('source, remove_whitespace, validate', [
    pytest.param(
        power.BACHELOR063_PDF,
        False,
        None,
        id='bachelor63_false',
    ),
    pytest.param(power.BACHELOR063_PDF, True, None, id='bachelor_true'),
    pytest.param(
        power.MASTER116_PDF,
        True,
        validate_master116,
        id='master116_true',
    ),
    pytest.param(power.MASTER072_PDF, False, None, id='master72_false'),
    pytest.param(power.MASTER072_PDF, True, None, id='master72_true'),
])
@utilatest.nightly
def test_text_mine_holy_whitespaces_remove(source, remove_whitespace, validate):
    # TODO: ADD MORE SINGLE PAGE VALIDATION
    pages = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    extracted = mine_holywhitespace(source, remove_whitespace, pages, 10)
    if validate:
        validate(extracted[0])


def mine_holywhitespace(source, remove_whitespace, pages, expected_length):
    config = rawmaker.parameter.ParsingConfiguration(
        boxes_flow=0.5,
        char_margin=1.0,
        line_margin=0.15,
        line_overlap=0.1,
        word_margin=0.01,
        strip=remove_whitespace,
    )
    extracted = rawmaker.features.text.extract_document(
        source,
        config=config,
        pages=pages,
    )
    assert len(extracted) == expected_length, extracted
    for page in extracted:
        text = [line.text.strip() for line in page]
        if remove_whitespace:
            assert all(len(line) for line in text), text
        else:
            # contains some holy white spaces
            holywhitespaces = [len(line) for line in text]
            assert not all(holywhitespaces), text
    return extracted


def test_text_no_char_horizontals_in_text():
    """Ensure that horizontals which are build out of '-' are not parsed
    as text, cause this will complicate further text processing."""
    parsed = rawmaker.features.text.work(
        power.BACHELOR128_PDF,
        pages=(7,),
    )
    document = serializeraw.load_document(parsed[0])
    counted = document.text.count('_')
    assert not counted
