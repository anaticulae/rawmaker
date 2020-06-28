# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

TABLE_HORIZONTAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=4.0).value
TABLE_VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=4.0).value


# tables are buld ouf long lines. The average line length is used to
# exclude figures etc.
TABLE_MIN_AVG_LINE_LENGTH = configo.HV_FLOAT_PLUS(40.0)
