# Changelog

Every noteable change is logged here.

## v2.17.3

### Fix

* do not replace umlaute (741808fefad2)
* add color spaces selector (c715facba0e9)

## v2.17.2

## v2.17.1

### Feature

* do not fail on outline extraction error (91fc865faf21)

### Fix

* remove senseless check (b1e0acf6cb44)
* handle drucksache correctly (337e42521461)

## v2.17.0

### Feature

* extend special char converter (6bc5e94b5df5)
* extend special char table (011dbe1eb7ca)
* improve color space detector (ea6ba9c708e5)

### Fix

* four items colorspace (e50d762b4d4c)
* skip broken image writer (469f0dc3659a)
* add gray color space (324f7cc53ebf)

## v2.16.0

### Feature

* add more special characters (24472345a67b)
* improve text part skipper (10580a1a9c0b)
* do not render any figure, just create figure border (4f1873549d9b)
* verify pdf binary header (a7c44a61ef8c)

### Fix

* adjust hidden figure skipper (36ea6a359ccf)
* add complex outlines parser (aafe67e5107b)
* extend outlines pattern (a3414ea1df77)
* catch invalid pdf header (6e7315589242)
* catch invalid encryption method (e2a5151468c2)
* handle pdfminer recursion error (dbee1a9f74dd)
* catch pdfminer pdf parsing error (c888dfa16ea1)
* log error instead of failing (b394a3afec47)
* fix crop box detector (4928d285d107)

## v2.15.0

### Feature

* add strict flag to fail pdfinfo on error (f0b47cd29e02)

### Fix

* disable unused cli parameter (ea43d9d1495d)
* extend outlines parser (d86642eb4458)

## v2.14.1

### Fix

* skip text only figures (0310e3fb0532)
* skip hidden rectangle (87067578a89c)
* skip hidden boxes with zero width lines (501bdf28e996)

## v2.14.0

### Feature

* add automation tool to run rawmaker over multiple pdfs (238f4bc9172b)

### Fix

* catch rawmaker png decoder error (e3a83df9586d)
* disable not required assertion (f4161ca32769)

## v2.13.2

### Feature

* increase number of lines to merge (c67216d7997a)
* add first draft of jbig2 image format (e88537c843f8)
* add support for external link outline (79443f23912f)

### Fix

* do not fail on negative font size (489afc921c1c)
* catch not supported export error (29c970be2879)
* ensure correct data type (cdaaf4790f06)
* skip invalid image renderer (41f34a441033)
* adjust broken unit test (d0c3c73038a4)

## v2.13.1

### Fix

* ensure that bounding box is merged correctly (c906ecf91942)

## v2.13.0

### Feature

* limit max lines per content page (0eb3036a818c)
* limit max figure size to save memory consumption (4897d4c16660)
* accept curves as lines (12a28dff3115)
* make merging orientation depended (2e7f2ac4c80e)

### Fix

* add workaround to pass tests, rework later (c8cf85a9de38)

## v2.12.1

## v2.12.0

### Feature

* disable figure check for figures with more than text (647b2a8967a1)
* make figure detector more optimistic (4164c4b57a18)

### Fix

* do not merge empty collected (1ecb584e5da5)

## v2.11.0

### Feature

* merge different table extractor strategies (c90331db3483)
* skip empty pages (bdfae4886ed4)
* add first optimizer to verify good rawmaker config (fcdba0935d9e)

## v2.10.3

### Fix

* shrink detected area to bounding box between chars (cd53825a1bff)

## v2.10.2

### Fix

* do not extract not selected pages (f96d039122a1)

## v2.10.1

### Fix

* add missing import (3b9b0e151111)

## v2.10.0

### Feature

* add wspace step to extract spaces between words (db4ae12eeadc)
* add basic skeleton of spacestation application (d239793a9ba5)

## v2.9.5

### Feature

* increase required logging level (68f1cac3a6e2)

### Fix

* fix error in single formula loader (f69b10876f96)
* fix starting virtual char bounding computation (e7dc0983ecaa)
* extend outlines to support FitH (ea883179d00c)

### Documentation

* Happy New Year! (c5999fa0b599)

## v2.9.4

## v2.9.3

## v2.9.2

### Fix

* add regression test to ensure prefix work step order (6c78dbea0777)
* adjust generated pages numbers (336a787a5402)
* fix skipping wrong images (53e0395b6b11)

## v2.9.1

## v2.9.0

### Feature

* parallelize horizontal step to improve performance (18e5d3252a74)
* add profiling information to table strategy steps (c36fe04f9879)
* fork strategy to reduce required runtime (151338e9bad1)
* improve long line formula decider (7fd0e314b758)
* improve formula extractor (c16365a84cf0)
* create bigger cluster to include more chars into formula (36250b1caf2b)

### Fix

* add missing imports (8ceca10e1ce9)
* support multiple characters in formula extraction (e6889e59c087)
* skip empty character to ensure dumper/loader works correctly (88cac3eebdc1)
* fix page number (2e1e103d5313)

## v2.8.2

### Feature

* remove duplicated lines which are produced by figure (bdc1d0236a8b)

## v2.8.1

### Feature

* add special image line detector (c6e72734ff86)

## v2.8.0

### Feature

* extend formula detector (9238198ea95f)
* improve formula detector (12c0dd45504a)
* extend formula bad list (df83af60ee66)
* accept lines printed in figures (d9542e3b747c)
* improve debug ability of FormulaRaw (a763a3a83557)
* adjust error message (183c3771d021)
* ensure that content equal images does not have the same hash (606320da74e5)
* add boxes and images as input for figure extractor (70f3c203c60d)

### Fix

* fix formula page numerator (77e522dc7dca)
* add backup table for char converter (0c584de8855e)
* add missing imports (5f95e68dac0d)

## v2.7.0

### Feature

* add option to remove char based horizontal lines (f5f1b105187b)

### Fix

* fix page number of first extract images page (0611e110da1e)
* skip big figures instead raising MemoryError (115a6bf5456a)

## v2.6.0

### Feature

* add wordbox parser (580309f26585)
* ease accessing text data (71f9b7ab24f9)
* add field access to bounding information (1794d65c8a25)
* add miner to parse single char layout (eafa2897f64b)

## v2.5.1

### Fix

* skip white spaces only object in border detection (8575f214be92)
* sort boundings before merging them (12435970fe32)

## v2.5.0

### Feature

* add pdfminer independent layout merger (61ab3477daf6)
* sort formula from top to down (9d7aae39e92e)
* add alpha char counter to exclude sentences from formula (905a0a25e717)
* improve formula parser (a09cd11c4b83)
* add non formula black list (84031fcd475f)

### Documentation

* document different test coverage of current release (5ae1a6214ac2)

## v2.4.1

## v2.4.0

### Feature

* split mixed horizontal/vertical text container (ef15e67d6030)
* return raw char value for pdf font parsing error (8b03f3d3715a)

### Fix

* skip and log invalid image (c7cd4bf67809)

## v2.3.0

### Feature

* clarify error message (d505c33d3758)
* make dumping format more readable (ac73cde505ba)
* add first draft of text figure renderer (a1b357238ffc)

### Fix

* group text bounding box correctly (dccdeced6e2a)
* fix bachelor37 font extraction (21717111cdf3)
* fix interface documentation (932dbcb4c1fd)
* sort formula character from left to right (f9ae962e87f7)
* solve font rise extraction bug (8e1d7d2f801a)
* handle failing tiff extraction (b257bd287bd7)

## v2.2.2

## v2.2.1

### Fix

* increase required debugging level (1211a9871333)

## v2.2.0

### Feature

* add formula extraction step (52ca713eb5dd)
* add first draft of formula extractor (9c1fa710c323)
* extend supported pattern (87e15c782e90)

## v2.1.3

### Feature

* add hook to gather additional complex figure data (7a227d3365ed)

## v2.1.2

## v2.1.1

## v2.1.0

### Feature

* use new file hash naming pattern (f366f0028746)

## v2.0.1

### Documentation

* remove empty changelog entrees (c1add919edb2)

## v2.0.0

### Feature

* move figure scaling to user interface (1a63fc314a29)
* add experimental image renderer (cf9912670e48)
* dump bounding information of figure (638a939da6ed)
* add first buggy figure renderer approach (3f7861dcc4e8)

### Fix

* fix and log negative figure dimension (99e7c0763a75)
* do not dump pages without tables (a7ed7eeae07d)

### Documentation

* extend module documentation (4645df32ede0)

## v1.25.0

### Feature

* make crossed more robust against false detection (ccd1a066bb13)
* improve table crossed parser (998273392a8a)
* add crossed table detection strategy (89e9aa3a2ad6)
* add vertical diff tolerance (afa6eba19aab)

### Fix

* adjust test, empty pages are skipped (7add92fafc1c)

### Documentation

* fix spelling error (7198363deb73)
* add table extraction strategy documentation (2854bba34735)

## v1.24.0

### Feature

* add second table extraction strategy (39ac911322bb)
* improve table extractor (d17898a7c905)
* add algorithm debugging information (7e36a286dd8e)
* merge table with are near together to a single table (fa17652faa75)
* add table validator (a826b3e657f2)

### Fix

* fix test after changing dumping behavior (6359ba9ee239)
* do not skip empty result (d3f3e3d09b73)

## v1.23.0

### Feature

* exclude small, not possible tables (ebe6cf957272)
* use lines for small tables (40efab55e0d1)
* remove very short lines (35dc7a4ebb18)
* improve line merger to reduce potential line count (4d54a0360aff)
* support single line content table (14723045e9b3)
* improve bucket implementation (104b657758ac)
* use a new table detection approach (9b89c57ef302)
* add algorithm to extract tables (e8d794004d0d)

### Fix

* fix percentage computation (91f4106e1604)

## v1.22.6

## v1.22.4

### Fix

* disable Roman style detection (6d489b762250)

## v1.22.0

### Feature

* add missing verbose flag (2217799cbfa3)

## v1.21.4

### Feature

* reduce required runtime (5a7c75081dec)
* move horizontals to a separate rawmaker step (af22aa80bd1f)

## v1.21.3

### Fix

* handle more special chars correctly (acc5f751cb75)

## v1.21.2

### Fix

* fix bad printed text mining (3f00c5635b0d)
* fix importing order bug on runtime (ced7f4139c40)

## v1.21.0

### Feature

* merge divided lines together (923f2a0fbfcf)
* ensure top down, left right item order (f307d1866398)
* ensure (left, top, right, down) bounding order (063e0e87a48d)
* convert lines to tuple early (28347d2966fe)
* merge divided lines together (64b1b86bf4f2)
* improve font parser (f0beab61ad95)
* add error handler for not support outline parsing (d7baf488ef12)
* extend special char table (596909035898)

### Documentation

* add module documentation (1a6019b1b32d)

## v1.20.3

### Fix

* outline name is directly stored as bytes (aef1b913a2ab)
* add non reference page number (d565ad774125)

## v1.20.1

### Fix

* fix accessing list of filters (700ae2197323)
* detect missing meta information (2d65ebbce53c)
* use lower data keys (27272568e326)
* use PDFDocEncoding to encode correctly (85d1b13f0671)

## v1.20.0

### Feature

* add method to parse pdf dates (4f18e167e6e1)
* add meta data extraction to cli (45f6d8a5feb5)
* add method to parse pdf meta information (73518c3a690f)
* add option to choose output data format (eceecd241728)
* add pdfinfo to description (1b2f7266ae5a)
* add option to print validation result to console (7fa3e42fd3ed)

## v1.19.0

### Feature

* parse raw pdf page count to outlines (e7fa72e46925)
* add destination parser (9eedd85a2e59)
* rename `toc` to `outlines` step (14a33f75d452)
* introduce ImageInformation and solve naming conflict (ac59c5e9b4af)

### Fix

* fix accessing holy value (d11a98ea954c)

### Documentation

* add basic module documentation (82a914da2ba4)

## v1.18.3

### Feature

* log using fallback mode (d7590f92041a)

## v1.18.1

### Fix

* fix huge running path (afc7d25f5211)

## v1.18.0

### Feature

* add extraction to command line interface (78dccc6a3ee1)
* add method to dump raw figures and figure information (482b83188184)
* add method to extract bounding and position of figures (c8b42fa4b551)
* add basic cli structure and testing infrastructure (9a4589235124)

### Fix

* extend interface documentation (1abddf4d3db8)
* merge bounding of merged images correctly (20b45707cafd)
* allow tuple bounding boxes in images info analysis (ffbe900e13fd)

## v1.17.10

### Fix

* support tuple and BoundingBox (7d2be27f95b0)
* solve some problems with pdfminer text mining (ec63d576291c)
* filter duplicated lines (60c3c2e78fa4)

## v1.17.8

### Feature

* add path images determination method (d1d7bd785351)

## v1.17.7

### Fix

* fix text bounding computation (2ce04e8be0df)

## v1.17.6

### Feature

* compute mean height of text line (0209e6e55370)

### Fix

* fake char mean height to pass test (e8c2ca06375f)
* use correct coordinate (7cf7c3e6ae3d)

## v1.17.5

### Feature

* add threshold to avoid mini font rises (849ad787db4b)
* sort line data ascending by y-coordinate (cf25146878c3)

### Fix

* reduce min count of characters which represent a line (47c1f989b62a)
* use center of textual horizontal lines (5e94a2afe92b)

## v1.17.4

### Fix

* add missing flip of lines (63dab400fdb8)
* enable doctests (ebbf2053357d)

## v1.17.3

### Feature

* support specific data extension (c53ec340400f)

### Fix

* ensure to flip all chars correctly (ce9d9777129a)
* write page count as number instead of string (eac0e02b991c)
* do not fail if pdfinfo exists (4fef82e44cd2)
* ensure that malformed bounding let not fail extraction (9496445541b9)

## v1.17.1

### Feature

* store bounding of image in document (45fb2d77ef0c)
* pass extracted image to extract position information (5518c5a05153)
* add method to load image inforation (3ee9a1ea6534)

### Fix

* fix missing test resource (4f65bbf49462)
* check later cause data is generated (9df72ad96f8b)

## v1.17.0

### Feature

* we do not support pdf extraction flag (3ce6fba21574)
* decide that we support only a single input (f4d52f533a83)
* replace single flips due general flip (03fbf5f50e89)
* prepare flipped container to flip coordinates in parser (38a5fa4dabad)
* support dumping multiple images (63fd70702587)
* add step to extract image information (d2c0e26414d4)
* add ?optimizer? to improve image parsing speed (34efe8aa7567)
* skip unsupported broken loader (4bd3eaab1cd3)
* create temp folder only if required (bc01b890c29b)
* add step to rawmaker cli (6dd6577c8e68)
* catch errors on parsing images (40e7b086468e)
* support png, jpg and tiff (9a6b9edd20f8)
* support images to merge (b057ec9b241f)
* use pdfminer image extractor to extract images (3b0f927df16a)

### Fix

* fix jpg file extension (76c4a28b559a)
* fix accessing color space data (8a4d960d44fc)
* catch problems in rgb decoder (d64bfffbf30d)
* handle empty images (6c68cd2fe190)
* sort images correctly (482155237039)
* fix accessing holy values (debfc92f7508)
* logging is always possible (030ecceb1371)

## v1.16.0

### Feature

* add parsing vertical text (2080e059cb84)
* extract and serialize font flags (701978cda9ba)
* introduce concept of Raw`Item` to avoid duplicating information (29bfa2deec74)
* add module to parse font flag (354efa0855b0)
* add flag to activate vertical text extraction (bb9740d8af35)
* add parameter to parsing configuration (0923b8ce14c6)
* remove pdfminer dependency (c0d95c085aec)

### Fix

* do not fail, just log the error (e7ab675fae53)
* disable annotation parser (f597c01bfc90)
* add missing nostrip flag (df81414e7ec4)

## v1.15.1

### Feature

* enable passing config by file (459f81190298)

## v1.15.0

### Feature

* replace --strip with --nostrip (b5145126a4dd)
* add option --whitespace to print analyzed white space to stdout (d5c8ef7f0ca8)
* add first approach of white space optimizer (187a6ea85fc4)
* add method to determine count of white space (8c723020944b)
* add basic cli structure (9457e5f813e8)

## v1.14.1

### Fix

* fix left right order for layout detection (0c19c6282509)
* update TextContainer bounding boxes for stripped content (82638571f7b1)

## v1.14.0

### Feature

* close current release plan (eb222dae0655)

## v1.13.8

### Feature

* sort boxes and horizontal lines top-down and left-right (2bb544d5f1aa)

### Fix

* fix accessing holy values (d99e1985d6ae)

## v1.13.3

### Fix

* ensure parsing files without editor information (d2ef1d9b7e9f)

## v1.13.0

### Feature

* introduce new font index concept (1522c465e5bd)
* round to two digits to get a better accuracy (71c61779545b)
* ensure to handle strip and holy white spaces correctly (0ae35c739c03)
* round size and rise to reduce noise in logging (303fb4e4160c)

### Fix

* disable profiling in normal mode (305fdec852fa)

## v1.12.2

### Fix

* set correct rawmaker default strip value (7dc6599d70de)

## v1.12.0

### Feature

* set default strip to True and expose to global constant (c066921e6292)
* expose strip flag to cli (fa00f164b1c0)
* add `strip` flag to remove trailing white spaces/lines (8fcb245f99c8)

### Fix

* fix interface check (9a5a2c0ce1a5)

## v1.11.2

### Feature

* add path module to determine resource path (7209d3e83114)

## v1.11.1

### Fix

* add default empty result (1ca17c747cc7)

## v1.11.0

### Feature

* add interface for detect figure feature (772a9135b14f)
* add possible difference to cluster interface (81aeb4c51389)
* move rawmaker path from `hey` (f60aca1aaa36)
* add feature to extract potential tables (5c9a0fa59cbb)
* add method to determine the intersecting point of two lines (00b527f9f0ba)
* add linero to work with extracted lines (78a938f977b5)
* add method to extract and dump/load lines in document (fb245858ad9a)
* exclude non textual items out of text analysis (53bd92fe12c1)

### Fix

* add missing import (d27fb6a5f525)

### Documentation

* extend interface documentation (aeff59607fb3)
* remove duplicated todo, use backlog instead (8836f57e93b8)

## v1.10.0

### Fix

* ignore font snippet as suffix of font name (e4bdb2709e06)
* fix font determination bug in left right example (482cd9b1ec05)

### Documentation

* extend interface documentation (0f3e7ecd1106)
* extend interface documentation (22e2c1dd1ef0)

## v1.9.5

### Fix

* do not let font extraction fail, log error instead (3336c0529c23)

### Documentation

* merge double backlog (0c2524369919)
* remove unused documentation source (c85a6fc83a88)

## v1.9.4

### Fix

* flip y-coordinate of extracted BoundingBox (21c6cd90cc26)

## v1.9.0

## v1.8.1

### Feature

* add profile flag to measure working steps (8711d09fa819)
* add method to create LAParams out of Config (2c117fdd8235)
* add --sf to run super fast mode (63c994157c3d)
* add method to split iterable by chunk_size (de124477d936)
* extend help information (e9f5e3031925)

### Documentation

* extend interface documentation (4a99db050ef4)
* add readme how to profile rawmaker execution (64e7a78a2f3f)

## v1.8.0

### Feature

* support rotated pages (9bb86f764e97)
* add --status option to check validation result (c89b8c3631ea)

### Documentation

* extend interface documentation (81ad0759a253)

## v1.7.3

### Documentation

* Happy New Year! (4c6377472838)

## v1.7.2

### Fix

* handle broken input correctly (8a127968c083)

## v1.7.1

## v1.7.0

### Feature

* add console application to extract information out of pdf (5c943b658920)

### Documentation

* add code quality to current release plan (70699ef4d49f)

## v1.6.8

### Documentation

* add backlog to store list of further todos/ideas (d1c47432248f)

## v1.6.7

### Fix

* add more special character (437e096a043d)

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

## v1.4.1

### Feature

* add --linter flag to control result writing (ebdcb81d67cb)

## v1.4.0

### Feature

* add error handler to prepare user warning (c51f3e2dee81)

## v1.3.0

### Feature

* improve reading performance enormous (2da5eb6e15b9)

## v1.2.9

### Feature

* mine complete document in NIGHTLY tests (37060ad1e20a)

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

## v1.1.5

### Feature

* use multiprocessing to reduce single runtime (6e295f08f79d)

## v1.1.2

### Fix

* skip unsupported annotation (17fac8d0a655)

## v1.1.0

### Feature

* add external test data provider (52bbc6e3091e)

## v1.0.8

### Fix

* fix annotation parser to support reference lists (7325f4da8ed7)

## v1.0.2

### Feature

* log page with wrong horizontal line (930c30f4ed5c)

### Fix

* fix border cropping (91b665519ec7)

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
* support parametrization of single features (c199d821b0bb)
* improve grouping of sentences. Extend tolerance of failure (e73b500a19cc)
* add parametrization to text parsing (0cb048ae3b13)
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

## v0.4.3

### Feature

* add border extractor (75c7fb9ff538)
* add assertion to ensure parser interface (bb78fac81d5e)
* support mocking importlib (1e8c5ce5f2a2)
* add multiple return files to save in different files (6015936e0773)
* add bigger pdf file with empty page to coverer more cases (3a3a9aa55afd)
* catch error that pdf does not contains outlines (f445b4a181f8)

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
