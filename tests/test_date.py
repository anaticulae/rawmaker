# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import rawmaker.date


def test_parse_date():
    time = "D:20160419072554+02'00"
    parsed = rawmaker.date.parse(time)
    assert parsed.raw == time, parsed.raw
