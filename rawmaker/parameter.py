# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LAParams


def create_layout(char_margin: float):
    # char_margin = get(parameter, 'char_margin', default=5.0, min_value=0.1)
    # boxes_flow: 1.0 only the vertical position matters
    result = LAParams(char_margin=char_margin, boxes_flow=1.0)
    return result
