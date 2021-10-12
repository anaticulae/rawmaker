# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

TABLE_HORIZONTAL_DIFF_MAX = configo.HV_FLOAT_PLUS(default=4.0).value
TABLE_VERTICAL_DIFF_MAX = configo.HV_FLOAT_PLUS(default=4.0).value

# tables are buld ouf long lines. The average line length is used to
# exclude figures etc.
TABLE_LINE_LENGTH_AVG_MIN = configo.HV_FLOAT_PLUS(default=40.0)
