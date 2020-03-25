# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import letty.optimizer
import tests.resources


def test_optimizer():
    path = tests.resources.MASTER72
    pages = (3,)
    result = letty.optimizer.run(path, pages=pages, chars=10)
    assert result
