# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw


def parse(path: str) -> iamraw.PDFVersion:
    with open(path, mode='rb') as fp:
        loaded = fp.read(8)
        if not loaded[0:5] == b'%PDF-':
            return None
        loaded = str(loaded, encoding='ascii')
        major = int(loaded[5])
        minor = int(loaded[7:])
    return iamraw.PDFVersion(major, minor)
