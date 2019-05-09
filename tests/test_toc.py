# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from rawmaker import read
from rawmaker.error import MissingOutlines
from rawmaker.features.toc import work
from tests.resource import VIM_GUIDE_PDF


def test_toc_from_document_no_outlines(monkeypatch):
    """Remove outlines from pdf document"""

    def get_outlines():
        raise MissingOutlines()

    with monkeypatch.context():
        with read(VIM_GUIDE_PDF) as document:
            document.get_outlines = get_outlines
            work(document)
