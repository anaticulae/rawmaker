#!/usr/bin/env python
#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

PACKAGES = [
    'letty',
    'letty.quality',
    'rawmaker',
    'rawmaker.converter',
    'rawmaker.features',
    'rawmaker.fonts',
    'rawmaker.images',
    'rawmaker.miner',
    'rawmaker.patch',
    'rawmaker.text',
    'spacestation',
    'spacestation.features',
]
ENTRY_POINTS = dict(console_scripts=[
    'letty = letty.cli:main',
    'rawmaker = rawmaker.cli:main',
    'rawmaker_automate = rawmaker.cli_automate:main',
    'rawmaker_cleanup = cleanup.cli:main',
    'spacestation = spacestation.cli:main',
])

if __name__ == "__main__":
    utila.install(__file__)
