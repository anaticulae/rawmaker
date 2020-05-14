# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfinfo.meta
import tests.resources


def test_pdfinfo_meta():
    resource = tests.resources.RESTRUCTURED_PDF
    meta = pdfinfo.meta.determine(resource)
    assert 'author' in meta
    assert 'title' in meta
    assert 'subject' in meta
