# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila
import utila.cli

import pdfinfo
import pdfinfo.data
import rawmaker.error


@utila.saveme
def main():
    parser = utila.cli.create_parser(
        [],
        version=pdfinfo.__version__,
        outputparameter=True,
        inputparameter=True,
        prefix=False,
    )
    args = utila.parse(parser)  # pylint:disable=W0612
    inpath, outpath = utila.sources(args, singleinput=True)
    inpath = inpath[0]  # TODO: SUPPORT MULTIPLE PATH
    if not os.path.isfile(inpath):
        utila.error(f'require valid file resource: {inpath}')
        return utila.INVALID_COMMAND
    assert os.path.exists(inpath), f'invalid inpath: {inpath}'

    try:
        parsed = pdfinfo.data.parse(inpath)
    except rawmaker.error.InvalidPDF:
        # not a valid pdf file
        parsed = None

    jsonify = '{}'
    if parsed is not None:
        jsonify = pdfinfo.data.jsonify(parsed)

    if os.path.isdir(outpath):
        outpath = os.path.join(outpath, 'pdfinfo.json')
    utila.file_create(outpath, jsonify)
    return utila.SUCCESS
