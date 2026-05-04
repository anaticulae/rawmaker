# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utilo


def underline_chars(
    document: iamraw.Document,
    underlinex: str = None,
    pages: tuple = None,
):
    # TODO: MARK HORIZONTAL AS TEXT UNDERLINE HORIZONTAL!
    # TODO: SUPPORT PARTIAL UNDERLINES
    # TODO: UPDATE STYLE RANGE AFTER SETTING ONLY SOME CHARS AS UNDERLINED
    # TODO: REPLACE UNDERLINE WITH STYLE(NONE, UNDERLINE, CROSSED, OVERLINED)
    if not utilo.exists(underlinex):
        utilo.log(f'missing underlines: {underlinex}, skipping char underline')
        return document
    underlinex = serializeraw.load_horizontals(
        underlinex,
        pages=pages,
    )
    for pdfpage in underlinex:
        underlines, pagenumber = pdfpage.content, pdfpage.page
        current_page = utilo.select_page(document.pages, page=pagenumber)
        if not current_page:
            continue
        for underline in underlines:
            for textcontainer in current_page:
                if not underlined(textcontainer.box, underline.box):
                    continue
                # TODO: REMOVE APPEND AFTER SHRINKING TEXTCONTAINER TO
                # SINGLE LINE
                # update chars
                for char in utilo.flat(textcontainer, append=True):
                    char.underline = True
                break
    return document


def underlined(text: utilo.Rectangle, horizontal: utilo.Rectangle) -> bool:
    # TODO: SUPPORT CROSSED ETC.
    hline_inside = text[1] < horizontal[1] < text[3]
    if not hline_inside:
        return False
    near_bottom = utilo.near(
        expected=text[3],
        current=horizontal[1],
        diff=3.0,
    )
    if not near_bottom:
        return False
    # start and end of horizontal and text matches
    leftright = utilo.near(text[0], horizontal[0], diff=5.0)
    leftright &= utilo.near(text[2], horizontal[2], diff=5.0)
    if not leftright:
        return False
    return True
