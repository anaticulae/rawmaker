# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

Version = collections.namedtuple('Version', 'major minor')


def parse(path: str) -> Version:
    with open(path, mode='rb') as fp:
        loaded = fp.read(8)
        if not loaded[0:5] == b'%PDF-':
            return None
        loaded = str(loaded, encoding='ascii')
        major = int(loaded[5])
        minor = int(loaded[7:])
    return Version(major, minor)
