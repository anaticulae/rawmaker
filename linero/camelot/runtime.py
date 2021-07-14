# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import serializeraw
import utila

import linero.table.camelot

if __name__ == "__main__":
    FILE, PAGES = sys.argv[1], sys.argv[2]
    # TODO: REPLACE AFTER UPGRADING UTILA
    PAGES = utila.parse_numbers(PAGES.replace('_', ' '))
    result = linero.table.camelot.run(FILE, PAGES)
    dumped = serializeraw.dump_tables(result)
    utila.log(dumped)
