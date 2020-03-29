# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import letty.optimizer
import tests.resources


@utila.skip_longrun
def test_optimizer():
    path = tests.resources.MASTER72
    pages = (3,)
    result = letty.optimizer.run(path, pages=pages, chars=10)
    assert result


@utila.skip_longrun
def test_optimizer_hardtoread():
    path = tests.resources.BACHELOR37
    pages = (6,)
    result = letty.optimizer.run(
        path,
        pages=pages,
        chars=4,
        lines=10,
        # words=10,
    )
    assert result
