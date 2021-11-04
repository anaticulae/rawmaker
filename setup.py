#!/usr/bin/env python
#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md'), encoding='utf8') as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'rawmaker/__init__.py'), encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), encoding='utf8') as fp:
    REQUIRES = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='kiwi@derspanier.de',
        description='Covert PDF to raw data',
        install_requires=REQUIRES,
        long_description=README,
        name='rawmaker',
        platforms='any',
        url='https://rawmaker.dev.packages/checkitweg.de',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'letty',
            'letty.quality',
            'linero',
            'linero.camelox',
            'linero.features',
            'linero.table',
            'pdfinfo',
            'rawmaker',
            'rawmaker.cleanup',
            'rawmaker.cleanup.features',
            'rawmaker.cleanup.translate',
            'rawmaker.converter',
            'rawmaker.features',
            'rawmaker.fonts',
            'rawmaker.images',
            'rawmaker.miner',
            'rawmaker.patch',
            'rawmaker.text',
            'spacestation',
            'spacestation.features',
        ],
        entry_points={
            'console_scripts': [
                'letty = letty.cli:main',
                'linero = linero.cli:main',
                'pdfinfo = pdfinfo.cli:main',
                'rawmaker = rawmaker.cli:main',
                'rawmaker_automate = rawmaker.cli_automate:main',
                'rawmaker_cleanup = rawmaker.cleanup.cli:main',
                'spacestation = spacestation.cli:main',
            ],
        },
    )
