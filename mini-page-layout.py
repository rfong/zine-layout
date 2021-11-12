#!/usr/bin/python -O
'''
Script to generate TeX documents to conglomerate a printable PDF from a
PDF with a smaller page-size, meant to be folded and cut from double-sided
A4 or letter paper.

Example usage: input PDF is A7 size in portrait mode
    `python mini-page-layout.py input.pdf --folds=3`

Example usage: input PDF is 1/8-letter size in portrait mode
    `python mini-page-layout.py input.pdf --folds=3 --letter`

Example usage: input PDF is A7 size in landscape mode
    `python mini-page-layout.py input.pdf --folds=3 --landscape`

only actually tested for A7 lolol
'''
from enum import Enum
import math
from optparse import OptionParser
import os
import PyPDF2


MAX_FOLDS = 3
TEX_EXT = ".tex"

class PaperFormat(Enum):
    A4 = 1
    LETTER = 2

A4_FOLDS_TO_OUTPUT_FORMAT = {
    # 1-indexed
    1: "a4",
    2: "a5",
    3: "a6",
}

LETTER_FOLDS_TO_DIMENSIONS = {
    # 1-indexed
    # (width, height)
    1: (11, 8.5),
    2: (8.5, 5.5),
    3: (5.5, 4.25),
}

def get_num_pdf_pages(fname):
    reader = PyPDF2.PdfFileReader(open(fname, 'rb'))
    return reader.getNumPages()

def get_layout_tex(
    from_fold_level, from_filename, num_pages, format=PaperFormat.A4, is_portrait=True):
    '''
    Return TeX text to conglomerate a smaller (folded) PDF into the next
    size up, e.g. to assemble an A4 from an A5 PDF.
    :param from_fold_level: number of A4 folds to reach input file paper size
    :param from_filename: input filename
    :num_pages: page signature of input file
    :is_portrait: whether the INPUT file is in portrait mode
    :returns: TeX layout to compile the input PDF to the next paper size up
    '''
    mode = "landscape," if not is_portrait else ""
    if format == PaperFormat.A4:
        docclass = A4_FOLDS_TO_OUTPUT_FORMAT[from_fold_level]+"paper,landscape"
        return A4_LAYOUT_TEMPLATE % (docclass, mode, num_pages, from_filename)
    else:
        width, height = tuple([(str(x) + "in") for x in LETTER_FOLDS_TO_DIMENSIONS[from_fold_level]])
        return LETTER_LAYOUT_TEMPLATE % (
            width,
            height,
            mode,
            num_pages,
            from_filename)

# Parameterized TeX templates to assemble a PDF into the next paper size up
A4_LAYOUT_TEMPLATE='''\documentclass[%s]{article}
\\usepackage[final]{pdfpages}
\\usepackage[margin=0in,heightrounded]{geometry}
\\begin{document}
\\includepdf[pages=-,nup=1x2,%ssignature=%d]{%s}
\\end{document}
'''

LETTER_LAYOUT_TEMPLATE='''\documentclass[landscape]{article}
\\usepackage[final]{pdfpages}
\\usepackage[paperwidth=%s,paperheight=%s,margin=0in,heightrounded]{geometry}
\\begin{document}
\\includepdf[pages=-,nup=1x2,%ssignature=%d]{%s}
\\end{document}
'''

def main():
    parser = OptionParser()
    parser.add_option("--folds", dest="num_folds", default=1, type=int,
                      help="max folds: %d"%MAX_FOLDS)
    parser.add_option("--landscape", dest="is_landscape",
                      default=False, action="store_true",
                      help="set if in landscape mode")
    parser.add_option("--a4", dest="is_letter_format",
                      default=True, action="store_false",
                      help="set if using A4 paper; default is letter")
    (options,args) = parser.parse_args()

    # Validation
    if not args:
        print("Expected filename of input PDF")
        exit(0)
    if not os.path.exists(args[0]):
        print("Path %s does not exist" % args[0])
        exit(0)
    if options.num_folds not in range(1, MAX_FOLDS+1):
        print("--folds should be an integer in the range [1,%d]" % MAX_FOLDS)
        exit(0)
    options.paper_format = (
        PaperFormat.LETTER if options.is_letter_format else PaperFormat.A4)

    # For page signature, round up to nearest upward 2^(folds+1)
    num_pages = get_num_pdf_pages(args[0])
    pages_per_sheet = math.pow(2, options.num_folds + 1)
    print("pages_per_sheet:", pages_per_sheet)

    # Subtract the negative modulus to pad up to a whole page signature
    num_pages = num_pages - (num_pages % -pages_per_sheet)

    # Generate and write intermediate TeX files
    path_base, path_ext = os.path.splitext(args[0])
    out_path = args[0]
    folds = options.num_folds
    is_landscape = options.is_landscape
    # Start from smallest fold and increase paper size
    while folds > 0:
        # Use most recent file as input to next larger paper size
        in_path = os.path.splitext(out_path)[0] + ".pdf"
        if options.is_letter_format:
            out_path = (
                path_base + "-" + A4_FOLDS_TO_OUTPUT_FORMAT[folds][1:]
                + TEX_EXT
            )
        else:
            out_path = (
                path_base + "-" + A4_FOLDS_TO_OUTPUT_FORMAT[folds] + TEX_EXT
            )
        with open(out_path, "w") as f:
            print("writing to:", out_path)
            f.write(
                get_layout_tex(
                    folds, in_path, num_pages, format=options.paper_format,
                    is_portrait=(not is_landscape)
                ))
        # Set up for next loop
        folds -= 1  # Decrement
        num_pages /= 2
        is_landscape = True  # Always landscape for assemblies


if __name__=="__main__":
    main()
    #run_dir = os.getcwd()
