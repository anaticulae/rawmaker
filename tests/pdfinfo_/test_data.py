# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfinfo.data
import tests.resources


def test_pdfinfo_data_jsonify():
    resource = tests.resources.TOC_PDF
    info = pdfinfo.data.parse(resource)

    jsoned = pdfinfo.data.jsonify(info)
    assert isinstance(jsoned, str), str(jsoned)
    assert 'latex' in jsoned
    assert 'version' in jsoned
    assert 'major' in jsoned
    assert 'pages' in jsoned
