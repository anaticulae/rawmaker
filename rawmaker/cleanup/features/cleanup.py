# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import rawmaker.cleanup.work


def work(
    postfix: str,
    inputs: str,
    outputs: str,
    prefix: str = '',
    pages: tuple = None,
):
    # POSTFIX as value first!
    rawmaker.cleanup.work.cleanup(
        inputs,
        outputs,
        prefix,
        postfix,
        pages=pages,
    )
    return utila.NO_RESULT
