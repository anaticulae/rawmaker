# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import os
import sys

import iamraw
import serializeraw
import serializeraw.fonts
import utila

import rawmaker.features.fonts
import rawmaker.fonts.parser

PROCESS = 'rawmaker_cleanup'
DESCRIPTION = """\
Load PageTextNavigators, figures and tables.

It removes text which is inside figures and or tables and writes
PageTextNavigators afterwards.
"""


@utila.saveme
def main():
    parameter = user_input()
    cleanup(*parameter)
    sys.exit(utila.SUCCESS)


def user_input() -> tuple:
    parser = argparse.ArgumentParser(
        prog=PROCESS,
        description=DESCRIPTION,
    )
    parser.add_argument(
        '-i',
        dest='inpath',
        default=os.getcwd(),
    )
    parser.add_argument(
        '-o',
        dest='outpath',
        default=os.path.join(os.getcwd(), 'outpath'),
    )
    parser.add_argument(
        '--prefix',
        dest='prefix',
        default='',
    )
    parser.add_argument(
        '--postfix',
        dest='postfix',
        default='',
    )
    parser.add_argument(
        '--pages',
        dest='pages',
        default='',
    )
    args = parser.parse_args()
    pages = utila.parse_pages(args.pages)
    choice = args.inpath, args.outpath, args.prefix, args.postfix, pages
    return choice


def cleanup(inpath, outpath, prefix: str = '', postfix: str = '', pages=None):
    ptn = serializeraw.create_pagetextnavigators_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
        sort=False,
    )
    fontstore = serializeraw.create_fontstore_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
    )
    text = iamraw.Document(dimension=ptn[0].pagesize)
    textpositions = []
    for page in ptn:
        children, posis = create_page(page, fontstore)
        content = iamraw.Page(
            children=children,
            page=page.page,
            dimension=page.pagesize,
        )
        positions = iamraw.PageContentTextPosition(
            page=page.page,
            content=posis,
        )
        text.append(content)
        textpositions.append(positions)
    # dump result
    dump_result(text, textpositions, outpath, postfix)


def dump_result(text, textpositions, outpath, postfix):
    # write document
    text_dumped = serializeraw.dump_document(text)
    utila.file_replace(
        iamraw.path.text(outpath, prefix=postfix),
        text_dumped,
    )
    textpositions_dumped = serializeraw.dump_textpositions(textpositions)
    utila.file_replace(
        iamraw.path.textposition(outpath, prefix=postfix),
        textpositions_dumped,
    )
    # write reduced font store
    fontstore, fontcontent = rawmaker.features.fonts.parse_fonts(text)
    dumped_header = serializeraw.dump_font_header(fontstore)
    utila.file_replace(
        iamraw.path.fontheader(outpath, prefix=postfix),
        dumped_header,
    )
    dumped_content = serializeraw.dump_font_content(fontcontent)
    utila.file_replace(
        iamraw.path.fontcontent(outpath, prefix=postfix),
        dumped_content,
    )


def create_page(page, fontstore: iamraw.FontStore) -> iamraw.Page:
    if not page:
        return [], {}
    lines, positions = [], []
    for item in page:
        line = create_line(item, fontstore)
        lines.append((item.line, line))
        position = iamraw.TextPosition(
            bounding=item.bounding,
            mean=item.bounding_mean,
        )
        positions.append(position)
    container, positions = merge_neighbors(lines, positions)
    positions = {index: item for index, item in enumerate(positions)}
    return container, positions


def merge_neighbors(lines, positions):
    container, current = [lines[0][1]], lines[0][0]
    textpositions = [positions[0]]
    for ((number, line), texpos) in zip(lines[1:], positions[1:]):
        if (number - current) == 1:
            # merge
            before = container[-1]
            # add content
            before.lines.extend(line.lines)
            # update rectangle
            before.box = utila.rectangle_max((before.box, line.box))
            # merge textpositions
            textpositions[-1] = iamraw.TextPosition(
                bounding=tuple(before.box),
                mean=textpositions[-1].mean,
            )
            # update last line id to merge further items
            current = number
        else:
            # add new one
            container.append(line)
            textpositions.append(texpos)
            # reset merger
            current = 0
    return container, textpositions


def create_line(item, fontstore: iamraw.fontstore) -> iamraw.line:
    line = iamraw.TextContainer(box=item.bounding)
    style = item.style.content
    sizes = utila.flatten([
        (item.end - item.start) * [item.size] for item in style
    ])
    rises = utila.flatten([
        (item.end - item.start) * [item.rise] for item in style
    ])
    fonts = utila.flatten([
        (item.end - item.start) *
        [rawmaker.fonts.parser.font_toraw(fontstore[item.font])]
        for item in style
    ])
    flags = utila.flatten([
        (item.end - item.start) *
        [serializeraw.fonts.toflag(fontstore[item.font].flags)]
        for item in style
    ])
    chars = [
        iamraw.Char(
            value=value,
            size=size,
            rise=rise,
            font=font,
            flags=flag,
        ) for value, size, rise, font, flag in zip(
            item.text,
            sizes,
            rises,
            fonts,
            flags,
        )
    ]
    line.append(iamraw.Line(chars=chars, box=item.bounding))
    return line
