# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@pytest.mark.usefixtures('td')
@utilatest.longrun  # requires installed package
def test_cli_superfast(mp):
    source = power.DOCU027_PDF
    cmd = f'--sf -i {source} --text'
    tests.run(cmd, mp=mp)


@utilatest.nightly  # requires installed package
def test_cli_superfast_compare(td, mp):
    """Ensure that --superfast produces the same results as normal mode."""
    source = power.DOCU027_PDF
    first = td.tmpdir.join('first')
    second = td.tmpdir.join('second')
    # prepare
    td.mkdir('first')
    td.mkdir('second')
    # run
    with utila.chdir(first):
        cmd = f'--sf -i {source} --text'
        tests.run(cmd, mp=mp)
    with utila.chdir(second):
        cmd = f'-i {source} --text'
        tests.run(cmd, mp=mp)
    # compare
    ftext = utila.file_read(first.join('rawmaker__text_text.yaml'))
    stext = utila.file_read(second.join('rawmaker__text_text.yaml'))
    assert ftext == stext
    first_pos = utila.file_read(first.join('rawmaker__text_positions.yaml'))
    second_pos = utila.file_read(second.join('rawmaker__text_positions.yaml'))
    assert first_pos == second_pos
