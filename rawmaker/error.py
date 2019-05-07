#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================


class RawMakerError(Exception):
    """Parent class for user errors or input errors.

    Exceptions of this type are handled by the command line tool
    and result in clear error messages, as opposed to backtraces.
    """


class TextExtractionNotAllowed(RawMakerError):
    pass


class InvalidPDF(RawMakerError):
    pass
