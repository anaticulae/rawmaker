# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import pdfminer.layout
import pdfminer.pdffont


class PatchedLTChar(pdfminer.layout.LTChar):

    # pylint:disable=R0913
    def __init__(self, matrix, font, fontsize, scaling, rise, text, textwidth,
                 textdisp, ncs, graphicstate):
        super().__init__(matrix, font, fontsize, scaling, rise, text, textwidth,
                         textdisp, ncs, graphicstate)
        if fontsize == 1:
            # HACK: CLARIFY WHAT IS CORRECT, we need more generated pdf
            # examples
            self.fontsize = self.size
        else:
            self.fontsize = fontsize
        self.rise = rise
        self.flags = font.flags


def vertical(item: pdfminer.layout.LTChar) -> bool:
    """Check LTChar.upright flag."""
    with contextlib.suppress(AttributeError):
        if not item.upright:
            return True
        return False
    return None


def render_char(  # pylint:disable=W9015,W9016
        self, matrix, font, fontsize, scaling, rise, cid, ncs,
        graphicstate) -> PatchedLTChar:
    """Patch LTChar to introduce fontsize hack.

    Args:
        cid(int): character number id - ascii
        ncs(PDFColorSpace): colorspace of document
    Returns:
        Patched char object.
    """
    try:
        text = font.to_unichr(cid)
        assert isinstance(text, str)
    except pdfminer.pdffont.PDFUnicodeNotDefined:
        text = self.handle_undefined_char(font, cid)

    textwidth = font.char_width(cid)
    textdisp = font.char_disp(cid)

    # patch to document font size and rise
    item = PatchedLTChar(matrix, font, fontsize, scaling, rise, text, textwidth,
                         textdisp, ncs, graphicstate)
    self.cur_item.add(item)
    return item.adv
