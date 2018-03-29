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
Local aligment calculated via the BLAST restful API hosted by NCBI.

----
## Thanks