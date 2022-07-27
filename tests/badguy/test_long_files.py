# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import jam
import pytest
import utilatest

import tests


@utilatest.nightly
@pytest.mark.security
def test_badguy_longpdf_rawmaker(td, mp):
    very_long = os.path.join(td.tmpdir, 'balong.pdf')
    jam.write_blank_pdf(1000, very_long)

    tests.run(f'-i {very_long} -j=8', mp=mp)
