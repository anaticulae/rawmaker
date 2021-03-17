# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import rawmaker.features
import rawmaker.parameter


def test_toc_parametrization():
    """Test parametrization to get good result when parsing table of content

    This test is more for finding a good parameter, than for really testing.
    TODO: Improve this later. Don't know how to, yet.
    """
    with rawmaker.reader.read(power.DOCU27_PDF) as pdf:
        # Diff between chars which build a word
        config = rawmaker.parameter.ParsingConfiguration(char_margin=10.0)
        document = rawmaker.features.extract_content(pdf, config=config)
    page_with_toc = document[2]
    assert page_with_toc
