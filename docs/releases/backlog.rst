.. _backlog:

backlog
=======

* improve speed: half multicore runtime

* support --sf function for slowest four steps

* test_run_huge use tests.run_success to increase code coverage

* add extractor to extract cluster of lines as figures

* math extractor

* fix dirty annotation parser!

* add hidden whitespace parser

* Imagero (planned)

* support rotated pages, see master116

* add black and white analysis, move to image analysis package? Make this
  optional in GUI to let the user check if paper is black and white
  printable.

Math detector
-------------

* detect areas of math formulars

* run char-based analysis on math area

* add feature to merge different layout analysis: normal and char based
  for example

* Tabelero (planned)

* add step hidden_whitespace to extract list of hidden whitespaces

* add method to handle undefined character/ pdfminer. This is a source of
  characters which are longer than one!

* run pdfminer with settings.STRICT = True to collect implementation error

layout estimator
----------------

* add layout estimator to adjust text layout - let

font
----

* refactor old font behavior
