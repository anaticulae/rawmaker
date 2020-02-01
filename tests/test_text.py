#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import iamraw
import utila
from pytest import mark
from serializeraw import dump_document
from serializeraw import load_document

import rawmaker.features
import rawmaker.features.text
from rawmaker.features.text import work
from tests.resources import HELLO_WORLD_PAGES
from tests.resources import HELLO_WORLD_PDF
from tests.resources import VIM_GUIDE_PDF


def test_miner_pdf():
    parsed_file = work(VIM_GUIDE_PDF)
    assert parsed_file


def test_mine_hello_world_pdf():
    text, _ = work(HELLO_WORLD_PDF)
    loaded = load_document(text)

    assert loaded
    assert len(loaded) == HELLO_WORLD_PAGES


@mark.parametrize(
    'pdf_path',
    [
        HELLO_WORLD_PDF,
        VIM_GUIDE_PDF,
    ],
    ids=[
        'hello_world.pdf',
        'vimguide.pdf',
    ],
)
@utila.skip_longrun
def test_dump_and_load_pdf(pdf_path):
    """Parse text from pdf file and write the result. Load the result after
    and compare with item to save"""

    text = rawmaker.features.text.extract_document(pdf_path)
    assert text

    dumped = dump_document(text)

    loaded = load_document(dumped)

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
    parsed = work(VIM_GUIDE_PDF, pages=selected_pages)
    dumped_text, _ = parsed
    text = load_document(dumped_text)
    assert len(text) == len(selected_pages)
    text_page_numbers = [item.page for item in text]
    assert text_page_numbers == selected_pages, str(text_page_numbers)
