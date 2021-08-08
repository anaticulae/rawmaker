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
    args = parser.parse_args()
    choice = args.inpath, args.outpath, args.prefix, args.postfix
    return choice


def cleanup(inpath, outpath, prefix: str = '', postfix: str = ''):
    pages = (0,)
    ptn = serializeraw.create_pagetextnavigators_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
    )
    fontstore = serializeraw.create_fontstore_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
    )
    text = iamraw.Document(dimension=ptn[0].pagesize)
    text_positions = []
    for page in ptn:
        content = iamraw.Page(page=page.page, dimension=page.pagesize)
        positions = iamraw.PageContentTextPosition(page=page.page, content={})
        for index, item in enumerate(page):
            line = create_line(item, fontstore)
            content.append(line)
            positions.content[index] = iamraw.TextPosition(
                bounding=item.bounding,
                mean=item.bounding_mean,
            )
        text.append(content)
        text_positions.append(positions)
    # write document
    text_dumped = serializeraw.dump_document(text)
    utila.file_replace(
        iamraw.path.text(outpath, prefix=postfix),
        text_dumped,
    )
    textpositions_dumped = serializeraw.dump_textpositions(text_positions)
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


def create_line(item, fontstore: iamraw.FontStore) -> iamraw.Line:
    line = iamraw.TextContainer()
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
    line.append(iamraw.Line(chars=chars))
    return line
