# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo
import utilotest

import tests


@pytest.mark.usefixtures('td')
@utilotest.longrun  # requires installed package
def test_cli_superfast(mp):
    source = hoverpower.DOCU027_PDF
    cmd = f'--sf -i {source} --text'
    tests.run(cmd, mp=mp)


@utilotest.nightly  # requires installed package
def test_cli_superfast_compare(td, mp):
    """Ensure that --superfast produces the same results as normal mode."""
    source = hoverpower.DOCU027_PDF
    first = td.tmpdir.join('first')
    second = td.tmpdir.join('second')
    # prepare
    td.mkdir('first')
    td.mkdir('second')
    # run
    with utilo.chdir(first):
        cmd = f'--sf -i {source} --text'
        tests.run(cmd, mp=mp)
    with utilo.chdir(second):
        cmd = f'-i {source} --text'
        tests.run(cmd, mp=mp)
    # compare
    ftext = utilo.file_read(first.join('rawmaker__text_text.yaml'))
    stext = utilo.file_read(second.join('rawmaker__text_text.yaml'))
    assert ftext == stext
    first_pos = utilo.file_read(first.join('rawmaker__text_positions.yaml'))
    second_pos = utilo.file_read(second.join('rawmaker__text_positions.yaml'))
    assert first_pos == second_pos
