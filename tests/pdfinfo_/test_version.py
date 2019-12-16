# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pdfinfo.version
import tests.resources


def test_pdfinfo_parse_version():
    ressource = tests.resources.TOC_PDF
    parsed = pdfinfo.version.parse(ressource)

    assert parsed == pdfinfo.version.Version(1, 5), str(parsed)
