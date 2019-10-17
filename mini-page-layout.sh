#!/bin/bash
# Script to make a printable A4 or letter PDF from a PDF with a smaller page 
# size which is meant to be folded from a double-sided sheet.
# Example usage:
# 	`./mini-page-layout.sh zine-A7.pdf 3`
# 	`./mini-page-layout.sh -l zine-A7.pdf 3`

OUTPUT_DIR='output'
mkdir -p $OUTPUT_DIR

# Validation
if [[ -z "$1" ]]; then
	echo "Argument 1 should be the path of an input PDF."
	exit 1
fi
if [[ -z "$2" ]]; then
	echo "Argument 2 should be the number of times an A4 sheet is folded."
	exit 1
fi

while getopts "ltq" opt; do
  case $opt in
    l)  # Input file is in landscape mode.
			landscape=1
      ;;
		t)  # Test python file, but do not compile TeX
			nocompile=1
			;;
		q) # Quiet output of TeX compilation
			quiet=1
			;;
    #\?)
    #  echo "Invalid option: -$OPTARG" >&2
    #  exit 1
    #  ;;
  esac
done
shift "$((OPTIND-1))"  # Shift away opts
#echo "args: $@"

# Copy source file here
cp $1 $OUTPUT_DIR

# Get file basename
base_fname=$OUTPUT_DIR/${1%.*}

# Remove old intermediate TeX files
exts=("tex" "aux" "log")
for ext in ${exts[@]}; do
	[ -e "${base_fname}-a*.$ext" ] && trash "${base_fname}-a*.$ext"
done

# Generate new TeX files
if [ -z $landscape ]; then
	python mini-page-layout.py $1 --folds=$2
else
	python mini-page-layout.py $1 --folds=$2 --landscape
fi

if [ "$nocompile" ]; then
	echo "Skip compilation"
	exit
fi

# Compile TeX
for f in `ls ${base_fname}-*.tex | sort -r`; do
	if [ "$quiet" ]; then
		pdflatex $f >/dev/null
	else
		pdflatex $f
	fi
done

print "Wrote output to ${base_fname}-a4.pdf"
open ${base_fname}-a4.pdf
