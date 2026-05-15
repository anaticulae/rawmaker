# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# import os

# import hardcore
# import iamraw.path
# import pytest
# import serializeraw

# import tests

P50_SPD = """\
Sammelmappe2.pdf
    Europa
    Respekt
    Titel
    Zukunft\
"""

# @pytest.mark.parametrize(
#     'source, expected',
#     [
#         pytest.param(hardcore.H000_IMAGETEXT_6_PDF, 6, id='figuretext'),
#         pytest.param(hardcore.P50_SPD, P50_SPD, id='spdfile'),
#         pytest.param(hardcore.P100_GRUENE, None, id='gruene'),
#         pytest.param(hardcore.P0_DRUCKSACHE1900302, None, id='drucksache19302'),
#     ],
# )
# def test_imagetext_outlines(source, expected, td, mp):
#     """Regression test to load outlines `FitH` correctly."""
#     cmd = f'-i {source} --outlines'
#     tests.run(cmd, mp=mp)
#     source = iamraw.path.outlines(path=td.tmpdir)
#     assert os.path.exists(source)
#     loaded = serializeraw.load_toc(source)
#     assert any((
#         len(loaded) == expected,
#         str(loaded) == expected,
#         expected is None,
#     ))
