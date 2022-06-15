# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Line Extractor
==============

This module aims to extract lines out of pdf document.

Furthermore the lines are:
    * fixed in x0/x1 and y0/y1
    * sorted from top to bottom and left to right
    * if required merged together.
"""

import operator
import typing

import configo
import iamraw
import pdfminer.layout
import pdfminer.pdfdocument
import serializeraw
import utila

import rawmaker.reader

# maximal difference in y-component
HORIZONTAL_DIFF_MAX = configo.HV_FLOAT_PLUS(default=2.0)
# maximal difference in x-component
VERTICAL_DIFF_MAX = configo.HV_FLOAT_PLUS(default=2.0)
# minimal number of minus signs which build a horizontal line
REQUIRED_MINUS_SIGNS = configo.HV_INT_PLUS(default=40)


def work(document: str, annotations: str, pages: tuple = None) -> str:
    if utila.exists(annotations):
        annotations = serializeraw.load_annotations(annotations, pages=pages)
    else:
        utila.error(f'missing {annotations} could not skip underlines')
        annotations = []
    with rawmaker.reader.read(document) as pdf:
        extracted = determine_lines(pdf, pages=pages)
    extracted = skip_lines(extracted, annotations)
    dumped = serializeraw.dump_lines(extracted)
    return dumped


def determine_lines(
    document: pdfminer.pdfdocument.PDFDocument,
    pages: tuple = None,
) -> iamraw.PageContentLines:
    lines_ = lines(document, pages=pages)
    result = []
    for content, number in lines_:
        # left point is left above from right down point
        content = [utila.rectangle_ensure_bounding(item) for item in content]
        # top down, left right
        content.sort(key=operator.itemgetter(1, 0))
        # merge lines which are divided by pdf printer
        merged = utila.merge_lines(content)
        result.append(iamraw.PageContentLine(content=merged, page=number))
    return result


def skip_lines(linex, annotation) -> list:
    result = []
    for page in linex:
        anno = utila.select_page(annotation, page.page)
        if not anno:
            result.append(page)
            continue
        invalid_area = [item.bounds for item in anno.hyperlinks]
        # remove annotated lines. This lines are the underlines of
        # hyperlinks which are produced by cray pdf printer.
        linex = [
            item for item in page.content
            if not utila.rectangles_intersecting(invalid_area, item)
        ]
        result.append(iamraw.PageContentLine(content=linex, page=page.page))
    return result


# do not merge near horizontal: '_______________' to text container below.
LAYOUT_LINES = pdfminer.layout.LAParams(line_margin=0.0000001)


def lines(
    pdf: pdfminer.pdfdocument.PDFDocument,
    pages: tuple = None,
) -> list:
    """Extract all `LTLine` out of `PDFDocument` page wise

    Support 3 different types of pdf layout elements:
        LTLine:
        LTRect: small difference between oposite lines
        LTTextBoxHorizontal:

    Args:
        pdf: pdf document to collect lines
        pages: select pages to run anlaysis on
    Returns:
        list of line objects[LTLine, LTRect, LTTextBoxHorizontal]
    """
    utila.asserts(pdf, pdfminer.pdfdocument.PDFDocument)
    possible_lines = type_in_document(
        pdf,
        datatype=(
            pdfminer.layout.LTTextBoxHorizontal,
            pdfminer.layout.LTLine,
            pdfminer.layout.LTRect,
            pdfminer.layout.LTFigure,
            pdfminer.layout.LTCurve,
        ),
        layout=LAYOUT_LINES,
        pages=pages,
    )
    strategy = {
        pdfminer.layout.LTLine: accept_ltline,
        pdfminer.layout.LTRect: accept_ltrect,
        pdfminer.layout.LTTextBoxHorizontal: accept_text_as_line,
        pdfminer.layout.LTCurve: accept_curve_as_line,
        pdfminer.layout.LTFigure: accept_figure_as_line,
    }
    result = []
    for content, pagenumber in possible_lines:
        page = []
        for item in content:
            # check item against strategy. If no stategy is supported, the
            # element is skipped.
            try:
                if not strategy[type(item)](item):
                    continue
                page.append(item)
            except KeyError:
                utila.error(f'unsupported strategy {item}')
        # convert bounding
        page = [(item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3])
                for item in page]
        # round bounding
        page = [utila.roundme(item) for item in page]
        # remove very short lines/dots
        page = [item for item in page if not utila.isdot(item, max_length=5.0)]
        # ensure left, top, right, down bounding
        page = [utila.rectangle_ensure_bounding(item) for item in page]
        # sort item top down; left right
        page.sort(key=operator.itemgetter(1, 0))
        # merges divided lines
        page = utila.merge_lines(page)
        # remove duplicated lines which mainly produces out of bad figure
        # extraction
        # TODO: ADD LINE DENSITY CHECK?
        page = utila.unique_lines(page, max_diff=3.0)
        result.append((page, pagenumber))
    return result


def accept_text_as_line(item: pdfminer.layout.LTTextBoxHorizontal):
    symbols = '_-='
    text = item.get_text()
    if len(text) < REQUIRED_MINUS_SIGNS:
        return False
    for symbol in symbols:
        if text.count(symbol) >= REQUIRED_MINUS_SIGNS:
            # update bounding to pass vertical error test.
            # use vertical centric position
            # TODO: CHECK THIS: Make it symbol dependend?
            if symbol in '_':
                ypos = utila.roundme(max((item.bbox[1], item.bbox[3])))
            else:
                ypos = utila.roundme((item.bbox[1] + item.bbox[3]) / 2)
            # update bounding box
            item.bbox = (item.bbox[0], ypos, item.bbox[2], ypos)
            return True
    return False


def accept_ltrect(item: pdfminer.layout.LTRect):
    return accept_ltline(item)


def accept_ltline(
    item: pdfminer.layout.LTLine,
    vertical_max_diff=VERTICAL_DIFF_MAX,
    horizontal_max_diff=HORIZONTAL_DIFF_MAX,
) -> bool:
    """Accept horizontal or vertical lines

    The lines must vary only little. A crossing line has vertical
    and horizontal error. We want | or - not / or \\.
    """
    assert item.bbox[3] >= item.bbox[1], str(item.bbox)
    assert item.bbox[0] <= item.bbox[2], str(item.bbox)

    horizontal_error = item.bbox[3] - item.bbox[1] >= horizontal_max_diff
    vertical_error = item.bbox[2] - item.bbox[0] >= vertical_max_diff

    if horizontal_error and vertical_error:
        return False

    if vertical_error:
        # HACK: WORKAROUND TODO:
        # horizontal lines: There are lines in bachelor028 which are
        try:
            blueline = BLUE in (item.stroking_color, item.non_stroking_color)
        except AttributeError:
            blueline = False
        if blueline:
            utila.debug('skip horizontal blue line which is may part of a '
                        'hyperlink and destroys footnote detection')
            utila.debug(item)
            return False
    return True


BLUE = [0, 0, 1]


def accept_figure_as_line(figure: pdfminer.layout.LTFigure) -> bool:
    """Some pdf renderer converts lines into images."""
    content = figure._objs  # pylint:disable=W0212
    if len(content) != 1:
        return False
    # Do we need a min width? I don't think so because thats the job of
    # later running methods.
    if accept_ltline(content[0]):
        return True
    if figure_special_line(figure):
        return True
    return False


def accept_curve_as_line(curve: pdfminer.layout.LTCurve) -> bool:
    pts = curve.pts
    if not curve.linewidth and not curve.fill:
        # invisible line
        return False
    if curve.stroke:
        if curve.stroking_color is None and curve.non_stroking_color is None:
            # TODO: DONT KNOW WHY
            return False
    if curve.fill:
        # polygon?
        if curve.height < 5.0 or curve.width < 5.0:
            return True
    if len(pts) == 2:
        # start and end point
        return True
    # more than two points in a row, check if point are on a line
    # [(437.04645, 259.38056), (437.04645, 293.26655), (437.04645, 269.60483999999997)]
    items = [(*first, *second) for first, second in zip(pts[:-1], pts[1:])]
    merged = utila.merge_lines(items, diff=1.5)
    if len(merged) == 1:
        # all lines in a row
        return True
    return False


# horizontal line which is rendered as a figure
HORIZONTAL_FIGURE_LINE_WIDTH_MIN = configo.HV_FLOAT_PLUS(default=350.0)
# the object have to be more width than height with this ratio
HORIZONTAL_FIGURE_LINE_RATIO_MIN = configo.HV_FLOAT_PLUS(default=45.0)


def figure_special_line(figure: pdfminer.layout.LTFigure) -> bool:
    """Detect special line and update figure box if figure is special line."""
    # TODO: THIS IS ONLY A HORIZONTAL?
    # EXAMPLE: MASTER155
    #  'width': 413.96, 'height': 8.54
    # TODO: ANALYZE IMAGE
    image = figure._objs[0]  # pylint:disable=W0212
    height = utila.rectangle_height(image.bbox)
    width = utila.rectangle_width(image.bbox)
    ratio = width / height
    if width <= HORIZONTAL_FIGURE_LINE_WIDTH_MIN:
        return False
    if ratio <= HORIZONTAL_FIGURE_LINE_RATIO_MIN:
        return False
    # adjust bounding of figure to middle line
    # TODO: USE IMAGE INFORMATION
    middle = utila.roundme((figure.bbox[1] + figure.bbox[3]) / 2)
    figure.bbox = (figure.bbox[0], middle, figure.bbox[2], middle)
    return True


def type_in_document(
    document: pdfminer.pdfdocument.PDFDocument,
    datatype: object,
    layout=None,
    pages: tuple = None,
) -> typing.List[typing.Tuple[pdfminer.layout.LTPage, int]]:
    """Extract defined `datatype` out of `PDFDocument`

    Args:
        document(PDFDocument): pdf document to extract all types
        datatype: selected item type
        layout(Param): process with different layout
        pages(tuple): select pages
    Returns:
        List with selected `datatype`.
    """
    utila.asserts(document, pdfminer.pdfdocument.PDFDocument)
    result = []
    for page in rawmaker.features.process_pagecontent(
            document,
            layout=layout,
            pages=pages,
    ):
        data = [item for item in page.content if isinstance(item, datatype)]
        result.append((data, page.page))
    return result
