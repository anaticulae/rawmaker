# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Layout Estimator Tool t.y.
==========================

Variation Strategy
------------------

Static
~~~~~~

Dynamic
~~~~~~~

Result: Points
~~~~~~~~~~~~~~

Judger
-------

Optimizer
---------

.. code-block:: none

    Optimizer -> Strategy -> Points -> Tool(Points) -> Result -> Judger(Result)
         !                     !                                     |
         !                     !                                     |
         < < < < < < < < < < <  < < < < < < < < < < < < < < < < < < </

"""

import os

import rawmaker

__version__ = rawmaker.__version__
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'letty'
