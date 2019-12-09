# Changelog

Every noteable change is logged here.

## v1.6.11

## v1.6.10

## v1.6.9

## v1.6.8

### Documentation

* add backlog to store list of further todos/ideas (d1c47432248f)

## v1.6.7

### Fix

* add more special character (437e096a043d)

## v1.6.6

## v1.6.5

## v1.6.4

## v1.6.3

## v1.6.2

## v1.6.1

## v1.6.0

### Feature

* determine rise for every character (72e8300e0c45)
* use new font size calculation feature (76cb26c88882)
* add font rise to mining result (ea0fd6838a11)
* patch pdfminer to gather font size and rise (6f72a972ab13)

### Fix

* split character which are grouped by layout parser (cbc54927f201)
* compare extracted test before saving (6ca5a8ad9aa4)
* use pageno of pdfminer correctly (3fd5afa3ca77)
* round Bounding coordinate to clarify coordinate (9fbdf877fbdb)

### Documentation

* extend documentation of mining class (49c562dadeae)

## v1.5.5

### Documentation

* setup doc strategy (835b290a82c8)

## v1.5.4

## v1.5.3

## v1.5.2

## v1.5.1

### Feature

* add feature to extract images (cc246a539bce)

### Fix

* resolve missing annotation reference (b266aa8aaeea)

## v1.5.0

### Feature

* support horizontal lines defined as string '__________' (b0758d9d4a5b)
* extend horizontal line detection (b4e3334e3988)

### Documentation

* add bug description when running with multiple cores on win (01fbeb82d4e4)

## v1.4.3

### Fix

* skip TextNotAllowed-Flag to avoid crash in analysis (25b10c166d36)
* catch annotation and log error - rework later (882cbfadbf5f)

## v1.4.2

## v1.4.1

### Feature

* add --linter flag to control result writing (ebdcb81d67cb)

## v1.4.0

### Feature

* add error handler to prepare user warning (c51f3e2dee81)

## v1.3.0

### Feature

* improve reading performance enormous (2da5eb6e15b9)

## v1.2.10

## v1.2.9

### Feature

* mine complete document in NIGHTLY tests (37060ad1e20a)

## v1.2.8

## v1.2.7

## v1.2.6

## v1.2.5

## v1.2.4

### Feature

* use serializeraw and make position page specific (e4ab4493c335)

## v1.2.3

### Feature

* add page selector to border feature (2c4c0a0eba4c)
* add page selector to border and boxes feature (96b07352652e)
* add page selector to annotation feature (e5aa7ae8f672)

## v1.2.2

### Feature

* make FontStore font indexing page independent (52f7fd6be1d4)
* add page limitation option to fonts extractor (ac319f674061)

## v1.2.1

### Feature

* add current page number to extracted pages (f202a94d6ac5)
* activate --pages flag to specify pages to extract (e221ad4de5ea)

## v1.2.0

### Feature

* extend font style parser to support type1, typ2 and mmfonts (baaab90e9707)

## v1.1.9

## v1.1.8

## v1.1.7

## v1.1.6

## v1.1.5

### Feature

* use multiprocessing to reduce single runtime (6e295f08f79d)

## v1.1.4

## v1.1.3

## v1.1.2

### Fix

* skip unsupported annotation (17fac8d0a655)

## v1.1.1

## v1.1.0

### Feature

* add external test data provider (52bbc6e3091e)

## v1.0.11

## v1.0.10

## v1.0.9

## v1.0.8

### Fix

* fix annotation parser to support reference lists (7325f4da8ed7)

## v1.0.7

## v1.0.6

## v1.0.5

## v1.0.4

## v1.0.3

## v1.0.2

### Feature

* log page with wrong horizontal line (930c30f4ed5c)

### Fix

* fix border cropping (91b665519ec7)

## v1.0.1

## v1.0.0

### Feature

* flip vertical y component (5d3f47b6d9b2)

### Documentation

* extend public interface documentation (177d7150ed81)

## v0.5.2

### Feature

* support mining explicit unicode chars (af94073521fa)
* group layout parameter into class (9a15194faccc)

### Fix

* fix container index of the last item on a page (36434bf2a2d6)
* fix negative font assertion (6bd5e226217f)
* extend parametrization of layout parser (7d9aa275c9ee)

### Documentation

* add hint to use `utila` cluster code (6b60245e5b1e)

## v0.5.1

### Feature

* add all feature to feature plan (4a6962e5f686)
* add parameter `char_margin` to support different configuration (aa5f34eadbdc)
* use new feature pack implementation (2c38d1af5c9d)
* use new featurepack/workplan syntax (1669f2f5b198)
* add annotation to extract page links and hyperlink (a898c19125b2)
* add method to process every single PDFPage of PDFDocument (bd1f05e3117a)
* ensure that font size is positive (d078cd3293cb)
* replace existing items, do not throw an error (f0eddbd074b1)
* add --prefix to separate output file names (781d4373ba4a)
* add Obli/Oblique as font type (3bc701bbac03)
* add min value to text extractor (bc6d7e44f337)

### Fix

* increase char_margin to avoid `single words` (b03f3a5066fe)
* use new feature interface (0ca8b7e6f147)
* remove verbose logging of bounding box and horizontal line (11b58d780a5d)
* change page numbers to zero based (e787d63bdaff)
* fix font size calculation - index error (617f74d199f6)
* font and text must use the same layout configuration (414f9168aa11)

### Documentation

* add documentation how extracted fonts are stored (28e82c08a6b1)

## v0.5.0

### Feature

* add parameter `char_margin` to `text` module (3f27eb52124e)
* add optional parameter to parameterize functions from outside (6ec7d3d6761a)
* support parameterization of single features (c199d821b0bb)
* improve grouping of sentences. Extend tolerance of failure (e73b500a19cc)
* add parameterization to text parsing (0cb048ae3b13)
* print usage of rawmaker when passing no arguments (74bedb3f05e6)

### Fix

* log missing toc as error to increase the importances (566076af4e43)
* rename output file to `boundingboxes` (4a286189a7e3)

## v0.4.9

### Feature

* support single pdf as input parameter (4abe865e0100)
* use BoundingBox instead of raw-representation (166af80c2cc8)
* add method to print content of DocumentItemHasher (e86f30b9edc3)
* add position as a sub feature of text (6e8b9e0c469a)
* add hasher to identify the position of object via hash-value (36e806731ed7)
* separate extracting the feature from dumping (ebc2549f771e)

### Fix

* add missing bbox to PageObject (561b5ac93c05)
* allow the empty string as a result from a feature (33f64ce67ff4)
* use `Flag` instead of useless shortcuts (ae6dfb889f3b)

### Documentation

* fix spelling and correct sentence (2eccf000cb20)
* extend documentation and fix spelling (fb8ffce9a186)

## v0.4.8

### Feature

* activate determine boxes and horizontal lines (1a380d191251)
* load and dump boxes and horizontal lines (49caf2878492)
* add method to process document content (1252fc1fb118)
* add parser to determine horizontal lines and boxes (1878858a48ca)
* add guard to cover all exceptions from pdf reader API (26eafd07e911)
* add feature interface for box parser functionality (bb0e2bee22d4)
* make feature scheduler more robust against broken interface (1fdff3f6667c)
* add converter to convert pixel in millimeter (918c856bbd66)

### Fix

* improve logging of collected items (eaf0ba45d006)
* fix BoundingBox of `iamraw`, remove after upgrade (07cb52336498)
* move file to correct location (d7f166bd5274)

## v0.4.7

### Feature

* extend parser to detect more types of style (b46ad9866882)

## v0.4.6

### Feature

* determine fonts for every character (1c7115820817)
* add font extractor/miner (f82e89ae2312)

## v0.4.5

## v0.4.4

## v0.4.3

### Feature

* add border extractor (75c7fb9ff538)
* add assertion to ensure parser interface (bb78fac81d5e)
* support mocking importlib (1e8c5ce5f2a2)
* add multiple return files to save in different files (6015936e0773)
* add bigger pdf file with empty page to coverer more cases (3a3a9aa55afd)
* catch error that pdf does not contains outlines (f445b4a181f8)

## v0.4.2

## v0.4.1

### Fix

* include requirements file to setup process (cb72ff105376)
* fix utila till using new release (fbc087d21b54)

## v0.4.0

### Feature

* remove vscode workspace, is generated by baw now (5132bd1a60f4)

### Fix

* add missing exception import (4b17cfa183b3)
* fix path to hello_world.pdf (c14c091fc9f8)

## v0.3.0

### Feature

* extract text out of pdf resource (96b60b8449ab)

### Fix

* add missing package url and clean up cmd interface (3a1d53d1b426)

## v0.2.0

### Feature

* include command and feature in delivery (c98279e3a59f)
* add commandline interface run to rawmaker (b5d8133000c1)
* add feature detector and move toc to features (7659e6dfb398)

### Fix

* clarify difference between package location and package name (10203af2cf2b)
* add missing code (25fc1bd581af)

## v0.1.1

### Feature

* add setup.py to build and deliver package (185dc1abe960)

## v0.1.0

### Feature

* dump/load table of content with yaml (b190939d0aa6)
* add table of content parser (92526652dd64)
* parsing of pdf files and basic error handling (0b484e30b2e7)
* add absolute file-ROOT to package (44cc011995d1)

## v0.0.0 Initial release

