#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from pytest import mark
from serializeraw import dump_document
from serializeraw import load_document

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

    assert loaded.page_count
    assert loaded.page_count == HELLO_WORLD_PAGES


@mark.parametrize(
    'pdf_resource', [
        HELLO_WORLD_PDF,
        VIM_GUIDE_PDF,
    ],
    ids=[
        'hello_world.pdf',
        'vimguide.pdf',
    ])
def test_dump_and_load_pdf(pdf_resource):
    """Parse text from pdf file and write the result. Load the result after
    and compare with item to save"""

    text, _ = work(pdf_resource)
    assert text

    loaded_yaml = load_document(text)
    another_dump = dump_document(loaded_yaml)

    assert another_dump == text


def test_text_mine_pdf_page_0():
    selected_pages = [3, 4, 5]
    parsed = work(VIM_GUIDE_PDF, pages=selected_pages)
    dumped_text, dumped_positions = parsed

    text = load_document(dumped_text)
    assert len(text) == len(selected_pages)

    text_page_numbers = [item.number for item in text]
    assert text_page_numbers == selected_pages, str(text_page_numbers)
