# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import jam
import utila

import tests
import tests.pdfinfo_


def test_badguy_longpdf_rawmaker(testdir, monkeypatch):
    very_long = os.path.join(testdir.tmpdir, 'balong.pdf')
    jam.write_blank_pdf(1000, very_long)

    tests.run_success(f'-i {very_long} -j=8', monkeypatch=monkeypatch)


@utila.skip_nightly
def test_badguy_longpdf_pdfinfo(testdir, monkeypatch):
    """Test that program success on very long, empty pdf file. Long
    files with content are catched by file size limit."""
    very_long = os.path.join(testdir.tmpdir, 'mejabalong.pdf')
    jam.write_blank_pdf(100000, very_long)

    tests.pdfinfo_.run_success(f'-i {very_long}', monkeypatch=monkeypatch)
