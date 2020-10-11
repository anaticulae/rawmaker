# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import pdfminer.layout
import utila

import rawmaker.converter.basic
import rawmaker.parameter


class MathConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self):
        super().__init__(laparams=LAYOUT)
        self.result = []

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)

        content = []
        for item in ltpage:
            rendered = render_pagecontent(item)
            if not rendered:
                continue
            content.extend(rendered)

        formulas = select_formulas(content)
        if not formulas:
            return
        pageformulas = iamraw.PageContentRawFormula(
            content=formulas,
            page=ltpage.pageid,
        )
        self.result.append(pageformulas)

    def close_document(self) -> iamraw.PageContentRawFormulas:
        result = list(self.result)
        self.result.clear()
        return result


# TODO: VERIFY THIS CONFIG
LAYOUT = pdfminer.layout.LAParams(
    line_overlap=0.3,
    line_margin=0.001,
    word_margin=0.0001,
    char_margin=5.0,
    detect_vertical=True,
)


def select_formulas(items):
    clustered = utila.same_line_cluster(
        items,
        max_diff=10,  # TODO: HOLY VALUE
        min_elements=4,
        matcher=lambda x: x[0][3],
    )
    result = []
    for cluster in clustered:
        content = cluster[:]
        # sort from left to right
        content = sorted(content, key=lambda x: x[0][0])
        text = ''.join([item[2] for item in content])
        if not isformula(text):
            continue
        formula = create_formula(content)
        result.append(formula)
    # sort formula top down by y1
    result.sort(key=lambda x: x.bounding[3])
    return result


def create_formula(items, page: int = None) -> iamraw.FormulaRaw:
    chars = [iamraw.MathChar(item[0], item[1], item[2]) for item in items]
    return iamraw.FormulaRaw(content=chars, page=page)


def render_pagecontent(item):
    """Collect all figures."""
    if not isinstance(item, pdfminer.layout.LTTextContainer):
        # Figure, line, etc.
        return None
    result = []
    lines = item._objs  # pylint:disable=W0212
    if len(lines) > 1:
        # multiline could not be a formular
        return None
    content = lines[0]
    if len(content) >= 50:
        # TODO: REPLACE THIS BAD SELECTOR
        return None
    # text = content.get_text().strip()
    # whitequote = len([item for item in text if item == ' ']) / len(text)
    for char in content._objs:  # pylint:disable=W0212
        if isinstance(char, pdfminer.layout.LTAnno):
            continue
        location = utila.roundme(tuple(char.bbox))
        text = char._text  # pylint:disable=W0212
        size = utila.roundme(char.size)
        result.append((location, size, text))
    return result


NO_FORMULA = r'\([ ]{0,2}\d{1,2}[ ]{0,2}\.[ ]{0,2}\d{1,2}[ ]{0,2}\)'


def isformula(text: str) -> bool:
    """\
    >>> isformula('Samples sind und ∆t die Samplingperiode')
    False
    >>> isformula('A^2+B^2 = C^')
    True
    >>> isformula('(3 .5 )')
    False
    >>> isformula('(a)')
    False
    """
    text = text.strip()
    if no_formula(text):
        return False
    if special_rate(text):
        return False
    if math_character(text):
        return True
    return False


ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def special_rate(text: str) -> bool:
    if len(text) < 20:  # TODO: HOLY VALUE
        return False
    alpharate = len([item for item in text if item in ALPHA]) / len(text)
    if alpharate > 0.8:  # TODO: HOLY VALUE
        return True
    return False


def no_formula(text: str) -> bool:
    if re.match(NO_FORMULA, text):
        return True
    if re.match(r'\([a-zA-Z]\)', text):
        # (a) (b)
        return True
    return False


def math_character(text: str) -> bool:
    if '=' in text:
        return True
    if '(' in text and ')' in text:
        return True
    if '·' in text:
        return True
    if '∆' in text:
        return True
    if '≤' in text:
        return True
    return False
