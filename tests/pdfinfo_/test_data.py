# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import pdfinfo.data


def test_pdfinfo_data_jsonify():
    resource = power.DOCU027_PDF
    info = pdfinfo.data.parse(resource)
    # dump it
    jsoned = serializeraw.dump_pdfinfo(info)
    assert isinstance(jsoned, str), str(jsoned)
    assert 'latex' in jsoned
    assert 'version' in jsoned
    assert 'major' in jsoned
    assert 'pages' in jsoned
