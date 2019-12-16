# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pdfinfo.info
import tests.resources


def test_pdfinfo_info_generator():
    ressource = tests.resources.TOC_PDF
    generator = pdfinfo.info.generator(ressource)

    assert generator == pdfinfo.info.Generator.Latex, str(generator)
