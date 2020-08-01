# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import iamraw
import pdfminer.layout
import utila

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
    clustered = same_line_cluster(items)
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
    if len(content) >= 20:
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


def same_line_cluster(
        todo,
        max_difference: float = 45.0,
        min_elements: int = 4,
):

    def classifier(candidat, clusteritem, max_difference=max_difference):

        def matcher(candidat, clusteritem):
            diff = math.fabs(candidat[0][3] - clusteritem[0][3])
            return diff <= max_difference

        return matcher(candidat, clusteritem)

    return utila.determine_cluster(todo, classifier, min_elements=min_elements)


def isformula(text: str) -> bool:
    """\
    >>> isformula('A^2+B^2 = C^')
    True
    """
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
