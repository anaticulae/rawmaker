# Error ticket - Broken annotation parser

This document is contains a pdf with version `PDF-1.5`. When the parser tries
to extract the page/link-annotations, the parser expects that the annotations
are stored in a list. On this document, the annotations are stored in a single
reference which contains the list.

## Workaround

This problem is solved by checking the list and if the reference is not a list
the single references is extracted to a list.

## Solved?

There is still a problem, cause I don't know why this single reference is
there.

## Resource

docu/porting_extension_modules.pdf
