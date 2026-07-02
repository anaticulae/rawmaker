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
import os
import sys

import configos
import utilo

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
                utilo.error(f'{future} failed.')
                utilo.error(error)
    return result


def run_single(path: str, pages: tuple, config: dict):
    config = ' '.join([f'--{key}={value}' for key, value in config.items()])
    pages_raw = ','.join([str(item) for item in pages])
    pages_raw = f'--pages={pages_raw}' if pages is not None else ''
    with utilo.make_tmpdir(root=configos.tmp()) as cwd:
        cmd = f'rawmaker -i {path} -o {cwd} {pages_raw} --text {config}'
        config_outpath = os.path.join(cwd, 'layout.ini')
        utilo.file_create(config_outpath, config)
        completed = utilo.run(cmd, cwd=cwd)
        if completed.returncode:
            utilo.error(f'could not run: {cmd}')
            utilo.error(completed.stdout)
            utilo.error(completed.stderr)
            sys.exit(utilo.FAILURE)
    quality = letty.quality.whitespace.determine(cwd, pages=pages)
    return OptimizerResult(quality, config)


def judge(result):
    ratio, best = result[0]
    utilo.log(result[0])
    for item in result[1:]:
        utilo.log(item)
        if item[0] < ratio:
            ratio, best = item
    return ratio, best


def strategy(
    chars: int = 10,
    words: int = 1,
    lines: int = 1,
    boxes: int = 1,
):
    boxes_flow = utilo.ranged_exp(0.5, 1.0, boxes)
    char_margin = utilo.ranged_exp(0.5, 20.0, chars)
    line_margin = utilo.ranged_exp(0.01, 5.0, lines)
    word_margin = utilo.ranged_exp(1.5, 5.0, words)
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
