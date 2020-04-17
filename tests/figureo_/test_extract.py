# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import figureo.extract
import tests.resources


def test_extract_figures():
    """2 Figures on page 12 and 1 figure and 1 image on page 13."""
    source = tests.resources.MASTER116
    pages = (12, 13)
    extracted = figureo.extract.extract_figures(source, pages=pages)
    assert extracted
    assert len(extracted) == 3, str(extracted)
