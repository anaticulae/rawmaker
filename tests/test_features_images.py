# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io

import pytest
import utila

import rawmaker.features.images
import tests.resources


@pytest.mark.parametrize(
    'pages, expected, filehash',
    [
        pytest.param(
            [14],
            [2],
            None,
            id='4bitimage',
        ),
        pytest.param(
            [10],
            [1],
            None,
            id='700subimages',
        ),
        pytest.param(
            None,
            None,
            None,
            id='complete',
        ),
        pytest.param(
            [9],
            [0],
            None,
            id='noimages',
        ),
        pytest.param(
            [55],
            [1],
            None,
            id='onepage',
        ),
        pytest.param(
            # algo will put 54 in front of 55
            [55, 56, 57, 60, 54],
            [1, 1, 1, 0, 2],
            [[-563269119, 1593581592], [-1359087221], [-491208895], [504237510]
            ],
            id='fourpages',
        ),
    ])
def test_features_images_extract_pages(
        pages,
        expected,
        filehash,
        testdir,
):
    source = tests.resources.BACHELOR_63_IMAGES
    extracted = rawmaker.features.images.extract_pages(source, pages=pages)
    if expected is not None:
        for page, expected_images in zip(pages, expected):
            assert len(extracted[page]) == expected_images, extracted[page]

    filehash = utila.flatten(filehash) if filehash else filehash
    written = 0
    for page, images in extracted.items():
        for index, (image, ext) in enumerate(images):
            fileoutpath = f'page{page}_{index}'
            if ext == 'png':
                rawdata = image._repr_png_()  # pylint:disable=W0212
            else:
                buffer = io.BytesIO()
                image.save(buffer, ext)
                rawdata = buffer.getvalue()

            with open(f'{fileoutpath}.{ext}', mode='wb') as output:
                output.write(rawdata)
            hashed = hash(rawdata)
            # if filehash:
            #     msg = (f'check {fileoutpath} the result seems to be wrong '
            #            '- if everything works fine, update expected file hash'
            #            f'{hashed}')
            #     assert hashed == filehash[written], msg
            written = written + 1
