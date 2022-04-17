.. _backlog:

backlog
=======

* improve speed: half multicore runtime

* support --sf function for slowest four steps

* test_run_huge use tests.run_success to increase code coverage

* math extractor

* fix dirty annotation parser!

* add hidden whitespace parser

* add black and white analysis, move to image analysis package? Make this
  optional in GUI to let the user check if paper is black and white
  printable.

Math detector
-------------

* add feature to merge different layout analysis: normal and char based
  for example

* add step hidden_whitespace to extract list of hidden white spaces

* add method to handle undefined character/ pdfminer. This is a source of
  characters which are longer than one!

* run pdfminer with settings.STRICT = True to collect implementation error

layout estimator
----------------

* add layout estimator to adjust text layout - let

font
----

* refactor old font behavior

pdfinfo
-------

* inform about using compatible mode, which requires more exection time

linero
------

* box matching is very slow, split into multiple core? Replace with
  better algo approach.

underlines
----------

* Decrease min horizontal line to detect very short underlined chars, may
  provide different horizontals loader for different approaches, introduce
  min_length while loading horizontals?

hyperlink lines
---------------

See bachelor028

<</S/URI/URI(http://www.europarl.europa.eu/factsheets/de/sheet/92/allgemeine-steuerpolitik)>>
endobj
109 0 obj
<</A 110 0 R /Border[ 0 0 0]/F 4/Rect[ 141 545 602 562]/Subtype/Link>>
endobj

The link and border is blue RGB (0,0,1) we have to investigate more
about Subtype/Link.
