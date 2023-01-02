# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import concurrent
import itertools
import math
import os
import sys

import configo
import utila

import letty.quality.whitespace

OptimizerResult = collections.namedtuple('OptimizerResult', 'value, config')
WORKER = 12


def run(
    path: str,
    pages: tuple = None,
    boxes: int = 1,
    chars: int = 10,
    lines: int = 1,
    words: int = 1,
    *,
    multicore: bool = True,
) -> OptimizerResult:
    todo = strategy(chars=chars, words=words, lines=lines, boxes=boxes)
    runner = threadpool if multicore else singlecore
    result = runner(todo, path, pages)
    judged = judge(result)
    return judged


def singlecore(todo: list, path: str, pages: tuple):
    result = []
    for config in todo:
        quality = run_single(path, pages, config)
        result.append(quality)
    return result


def threadpool(todo: list, path: str, pages: tuple):
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures = {
            executor.submit(run_single, path, pages, config): config
            for config in todo
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                quality = future.result()
                result.append(quality)
            except Exception as error:  # pylint:disable=broad-except
                utila.error(f'{future} failed.')
                utila.error(error)
    return result


def run_single(path: str, pages: tuple, config: dict):
    config = ' '.join([f'--{key}={value}' for key, value in config.items()])
    pages_raw = ','.join([str(item) for item in pages])
    pages_raw = f'--pages={pages_raw}' if pages is not None else ''
    with utila.make_tmpdir(root=configo.tmp()) as cwd:
        cmd = f'rawmaker -i {path} -o {cwd} {pages_raw} --text {config}'
        config_outpath = os.path.join(cwd, 'layout.ini')
        utila.file_create(config_outpath, config)
        completed = utila.run(cmd, cwd=cwd)
        if completed.returncode:
            utila.error(f'could not run: {cmd}')
            utila.error(completed.stdout)
            utila.error(completed.stderr)
            sys.exit(utila.FAILURE)
    quality = letty.quality.whitespace.determine(cwd, pages=pages)
    return OptimizerResult(quality, config)


def judge(result):
    ratio, best = result[0]
    utila.log(result[0])
    for item in result[1:]:
        utila.log(item)
        if item[0] < ratio:
            ratio, best = item
    return ratio, best


def strategy(
    chars: int = 10,
    words: int = 1,
    lines: int = 1,
    boxes: int = 1,
):
    boxes_flow = ranges(0.5, 1.0, boxes)
    char_margin = ranges(0.5, 20.0, chars)
    line_margin = ranges(0.01, 5.0, lines)
    word_margin = ranges(1.5, 5.0, words)
    result = []
    for char, word, box, line, in itertools.product(
            char_margin,
            word_margin,
            boxes_flow,
            line_margin,
    ):
        result.append({
            'boxes_flow': box,
            'char_margin': char,
            'word_margin': word,
            'line_margin': line,
        })
    return result


# TODO: REPLACE WITH UTILA CODE
def ranges(mini: float, maxi: float, steps: int = 15):
    """Compute parameter.

    >>> utila.roundme(ranges(0.1, 100, steps=10))
    [0.1, 0.12, 0.18, 0.34, 0.76, 1.92, 5.06, 13.61, 36.84, 99.99]
    >>> utila.roundme(ranges(0.1, 20, steps=5))
    [0.1, 0.73, 2.43, 7.06, 19.64]
    """
    func = math.exp
    maxed = func(steps - 1) / (maxi - mini)
    result = []
    for index in range(steps):
        value = mini + (math.exp(index) - 1) / maxed
        value = utila.roundme(value, digits=5)  # pylint:disable=R0204
        result.append(value)
    return result
