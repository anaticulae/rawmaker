#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import pytest
from tests.resource import HELLO_WORLD
from tests.resource import HELLO_WORLD_PAGES
from tests.resource import VIM_GUIDE

from rawmaker.features.text import work
from rawmaker.miner.mining import _dump_line
from rawmaker.miner.mining import _dump_page
from rawmaker.miner.mining import _dump_textcontainer
from rawmaker.miner.mining import _load_line
from rawmaker.miner.mining import _load_page
from rawmaker.miner.mining import _load_textcontainer
from rawmaker.miner.mining import dump_yaml
from rawmaker.miner.mining import Line
from rawmaker.miner.mining import load_yaml
from rawmaker.miner.mining import Page
from rawmaker.miner.mining import TextContainer
from rawmaker.reader import read


def test_load_and_dump_line():
    text = 'I am a Line'

    loaded = _load_line(text)

    assert len(loaded.chars) == len(text)

    dumped = _dump_line(loaded)

    assert dumped[1] == text


@pytest.fixture
def simple_textcontainer():
    container = TextContainer()
    container.lines.append(Line.from_str('I am a beautiful Line'))
    container.lines.append(Line.from_str('I am a more beautiful Line'))
    container.lines.append(Line.from_str('I am a the most beautiful Line'))
    return container


@pytest.fixture
def simple_page(simple_textcontainer):
    page = Page()

    page.children.append(simple_textcontainer)
    page.children.append(simple_textcontainer)
    page.children.append(simple_textcontainer)

    return page


def test_dump_and_load_textcontainer(simple_textcontainer):
    container = simple_textcontainer

    specifier, dumped = _dump_textcontainer(container)

    loaded = _load_textcontainer(dumped)

    assert loaded == container


def test_dump_and_load_page(simple_page):
    dumped = _dump_page(simple_page)
    loaded = _load_page(dumped)

    assert loaded == simple_page


def test_miner_pdf():

    with read(VIM_GUIDE) as pdf:
        parsed_file = work(pdf)


def test_mine_hello_world_pdf():
    with read(HELLO_WORLD) as pdf:
        data = work(pdf)

    loaded = load_yaml(data)

    assert loaded.page_count
    assert loaded.page_count == HELLO_WORLD_PAGES


@pytest.mark.parametrize('pdf_resource', [HELLO_WORLD, VIM_GUIDE])
def test_dump_and_load_hello_word(pdf_resource):
    with read(pdf_resource) as pdf:
        dumped = work(pdf)

    assert dumped
    # dumpped = dump_yaml(data)

    loaded_yaml = load_yaml(dumped)
    another_dump = dump_yaml(loaded_yaml)

    assert another_dump == dumped
