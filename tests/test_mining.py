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

from rawmaker import read
from rawmaker.features.text import work
from tests.resource import HELLO_WORLD_PAGES
from tests.resource import HELLO_WORLD_PDF
from tests.resource import VIM_GUIDE_PDF


def test_miner_pdf():
    with read(VIM_GUIDE_PDF) as pdf:
        parsed_file = work(pdf)
    assert parsed_file


def test_mine_hello_world_pdf():
    with read(HELLO_WORLD_PDF) as pdf:
        data = work(pdf)
    loaded = load_document(data)

    assert loaded.page_count
    assert loaded.page_count == HELLO_WORLD_PAGES


@mark.parametrize('pdf_resource', [HELLO_WORLD_PDF, VIM_GUIDE_PDF])
def test_dump_and_load_hello_word(pdf_resource):
    with read(pdf_resource) as pdf:
        dumped = work(pdf)
    assert dumped

    loaded_yaml = load_document(dumped)
    another_dump = dump_document(loaded_yaml)

    assert another_dump == dumped
