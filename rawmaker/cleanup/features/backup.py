# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def work(inputs: list, outputs, prefix: str = ''):
    if not outputs:
        outputs = inputs[0]
    prefixed = f'{prefix}_' if prefix else ''
    raw = f'rawmaker__{prefixed}'
    pattern = f'({raw}text|{raw}fonts|{raw}line|{raw}horizontals)_*.yaml'
    for inpath in inputs:
        utila.copy_content(
            inpath,
            outputs,
            pattern=pattern,
            rename=rename_backup,
        )
    return utila.NO_RESULT


BACKUP_EXT = 'baml'


def rename_backup(dest):
    dest = str(dest)
    dest = dest.replace('.yaml', f'.{BACKUP_EXT}')
    return dest
