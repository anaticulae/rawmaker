# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import camelot.handlers


def __init__(self, filepath, pages="1", password=None):
    self.filepath = filepath

    if password is None:
        self.password = ""
    else:
        self.password = password
        if sys.version_info[0] < 3:
            self.password = self.password.encode("ascii")
    self.pages = self._get_pages(self.filepath, pages)


# disable path check, we know what we do.
camelot.handlers.PDFHandler.__init__ = __init__
