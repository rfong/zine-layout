#!/bin/bash
# Script to make a printable A4 PDF from a PDF with a smaller page 
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

# Get file basename
base_fname=${1%.*}
echo $base_fname

# Generate new TeX files
if [ -z $landscape ]; then
	python mini-page-layout.py $base_fname.pdf --folds=$2
else
	python mini-page-layout.py $base_fname.pdf --folds=$2 --landscape
fi

# Remove old files
[ -e "$OUTPUT_DIR/${base_fname}-*" ] && trash "$OUTPUT_DIR/${base_fname}-*"

# Move TeX files to output dir
mv $base_fname-*.tex $OUTPUT_DIR
# Copy source file to output dir
cp $1 $OUTPUT_DIR

if [ "$nocompile" ]; then
	echo "Skip compilation"
	exit
fi

# Compile TeX
cd $OUTPUT_DIR
for f in `ls ${base_fname}-*.tex | sort -r`; do
	if [ "$quiet" ]; then
		pdflatex $f >/dev/null
	else
		pdflatex $f
	fi
done
cd ..

mv *.tex $OUTPUT_DIR >/dev/null
mv $base_fname-*.pdf $OUTPUT_DIR >/dev/null
[ -e "*.aux" ] && trash "*.aux"
[ -e "*.log" ] && trash "*.log"

cp $OUTPUT_DIR/${base_fname}-*4.pdf ${base_fname}-print.pdf
echo "Wrote output to ${base_fname}-print.pdf"
open ${base_fname}-print.pdf
open $OUTPUT_DIR/${base_fname}-a4.pdf
