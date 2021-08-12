# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os
import sys

import iamraw
import serializeraw
import serializeraw.fonts
import texmex
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
    todo = [
        utila.Flag(longcut='backup', message='write copy of source data'),
        utila.Parameter(longcut='postfix', message='rename output'),
    ]
    parser = utila.cli.create_parser(
        todo=todo,
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
            multiprocessed=False,
            pages=True,
            prefix=True,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        version=rawmaker.__version__,
        prog=PROCESS,
    )
    args = utila.parse(parser)
    choice = (
        args['input'][0],
        args['output'],
        args['prefix'],
        args['postfix'],
        utila.parse_pages(','.join(args['pages'])),  # DIRTY
        args['backup'],
    )
    return choice


BACKUP_EXT = 'baml'


def rename_backup(dest):
    dest = str(dest)
    dest = dest.replace('.yaml', f'.{BACKUP_EXT}')
    return dest


def cleanup(
    inpath,
    outpath,
    prefix: str = '',
    postfix: str = '',
    pages=None,
    backup: bool = False,
):
    if backup:
        prefixed = f'{prefix}_' if prefix else ''
        pattern = f'(rawmaker__{prefixed}text|rawmaker__{prefixed}fonts)_*.yaml'
        utila.copy_content(
            inpath,
            outpath,
            pattern=pattern,
            rename=rename_backup,
        )
    ptns = serializeraw.ptn_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
        sort=False,
    )
    # remove content here
    ptns = remove_skip_area(ptns, inpath, pages=pages)
    fontstore = serializeraw.create_fontstore_frompath(
        inpath,
        prefix=prefix,
        pages=pages,
    )
    document, textpositions, fontheader, fontcontent = dump_ptn(ptns, fontstore)
    write_result(
        outpath,
        document,
        textpositions,
        fontheader,
        fontcontent,
        postfix,
    )


def remove_skip_area(ptns, inpath: str, pages: tuple = None):
    imagepath = os.path.join(inpath, 'rawmaker__images_images')
    tableropath = iamraw.path.tablero_result(inpath)
    images = []
    if utila.exists(imagepath):
        images = serializeraw.load_image_infos_frompath(imagepath, pages=pages)
    tables = []
    if utila.exists(tableropath):
        tables = serializeraw.load_tables(tableropath, pages=pages)
    invalids = create_invalid_area(images, tables)
    for ptn in ptns:
        try:
            invalid_area = invalids[ptn.page]
        except KeyError:
            continue
        # line intersects with invalid area
        invalid_lines = [
            item for item in ptn
            if utila.rectangles_intersecting(invalid_area, item.bounding)
        ]
        for line in invalid_lines:
            ptn.remove(line)
    return ptns


def create_invalid_area(images, tables) -> dict:
    invalid = collections.defaultdict(list)
    for page in images:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in tables:
        invalid[page.page].extend([item.bounding for item in page.content])
    # reduce rectangle count
    result = {
        key: utila.rectangle_merge(value) for key, value in invalid.items()
    }
    return result


def write_result(
    outpath: str,
    document: iamraw.Document,
    textpositions: iamraw.TextPositions,
    fontheader: dict,
    fontcontent: list,
    postfix: str = '',
):
    utila.file_replace(
        iamraw.path.text(outpath, prefix=postfix),
        document,
    )
    utila.file_replace(
        iamraw.path.textposition(outpath, prefix=postfix),
        textpositions,
    )
    # write reduced font store
    utila.file_replace(
        iamraw.path.fontheader(outpath, prefix=postfix),
        fontheader,
    )
    utila.file_replace(
        iamraw.path.fontcontent(outpath, prefix=postfix),
        fontcontent,
    )


def dump_ptn(ptns: texmex.PageTextNavigators, fontstore: iamraw.FontStore):
    document = iamraw.Document(dimension=ptns[0].pagesize)
    textpositions = []
    for page in ptns:
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
        document.append(content)
        textpositions.append(positions)
    # write document
    dumped_document = serializeraw.dump_document(document)
    dumped_textpositions = serializeraw.dump_textpositions(textpositions)
    fontstore, fontcontent = rawmaker.features.fonts.parse_fonts(document)
    dumped_header = serializeraw.dump_font_header(fontstore)
    dumped_content = serializeraw.dump_font_content(fontcontent)
    return dumped_document, dumped_textpositions, dumped_header, dumped_content


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
    positions = dict(enumerate(positions))
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
    rotation = item.style.rotation
    if rotation:
        line = iamraw.VerticalTextContainer(box=item.bounding)
    else:
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
