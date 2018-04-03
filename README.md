# Sequence aligner

----
## Well, what is it?
This program allows you to align two strings, that may represent proteins, genes, or even just two strings you want to calculate the indel distance of.
See [Indel](https://en.wikipedia.org/wiki/Indel).

----
## Installation
Make sure you install all dependencies with:

    pip install -r requirements.txt

----
## Usage
1. Run the main.py file for a graphical interface.

----
## Features
Global alignment calculated offline using Needleman-Wunsch, can calculate multiple paths using linear or affine gap penalties.

Various other alignments calculated online using the EMBOSS RESTful API graciously hosted by EBI.

----
## Possible errors

### User input
There is some input validation present on the program GUI, however it is not extensive. The program mostly trusts the users input.

### XIO
On specific operative systems the multiprocessing module sometimes produces XIO fatal error 25. As the module is merely used to provide a comforting loading message commenting the lines containing the 'process' variable will resolve the issue without affecting the produced results.

### Error 400
Altough the EMBOSS server allows for the querying and use of its API, intensive use may get the provided default account temporarily banned. Changing the variable email1 in the emboss_align.py file to another valid email will likely solve this issue.


----
## Thanks
Rui Balau & Simon Afonso