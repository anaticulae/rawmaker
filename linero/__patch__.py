# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures

import utila


def fork(*runnables, worker: int = 6, process: bool = False) -> int:
    """Run methods in parallel."""
    failure = 0
    executor = concurrent.futures.ThreadPoolExecutor
    if process:
        executor = utila.select_executor()
    result = [None] * len(runnables)
    with executor(max_workers=worker) as pool:
        futures = {pool.submit(item): item for item in runnables}
        for future in concurrent.futures.as_completed(futures):
            index = runnables.index(futures[future])
            try:
                result[index] = future.result()
            except Exception as error:  # pylint:disable=broad-except
                utila.error(f'future number: {index}; {future} failed.')
                utila.error(error)
                failure += 1
    if failure:
        return failure
    return result


utila.fork = fork
