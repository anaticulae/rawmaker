# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import letty.optimizer


@utilatest.skip_longrun
def test_optimizer():
    path = power.MASTER072_PDF
    pages = (3,)
    result = letty.optimizer.run(path, pages=pages, chars=10)
    assert result


@utilatest.skip_longrun
def test_optimizer_hardtoread():
    path = power.BACHELOR037_PDF
    pages = (6,)
    result = letty.optimizer.run(
        path,
        pages=pages,
        chars=4,
        lines=10,
        # words=10,
    )
    assert result
