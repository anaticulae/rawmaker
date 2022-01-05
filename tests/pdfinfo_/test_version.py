# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power

import pdfinfo.version


def test_pdfinfo_parse_version():
    resource = power.DOCU027_PDF
    parsed = pdfinfo.version.parse(resource)
    assert parsed == iamraw.PDFVersion(1, 5), str(parsed)
