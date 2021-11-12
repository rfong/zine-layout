This script generates zine print layouts that are meant to be folded from double-sided A4 paper. I wrote it to streamline the A7 size [zines](https://distractibility.github.io) I sometimes make at home.

# Environment
Requires Python 3.

## Install packages
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Reactivate environment
```
source venv/bin/activate
```

# Usage

## Prep
Expected input: A PDF of your pages in sequential order, formatted as a page size you would get by folding a sheet N times (e.g. folding an A4 sheet into A5, A6, A7 size).

Name should be formatted to reflect page size: `*-A7.pdf`, `*-A6.pdf`, etc. The script may also have trouble if your input PDF is located outside this directory, so I recommend copying it in.
- [ ] TODO: make it so the name can be anything
- [ ] TODO: handle input file placement more cleanly

### Physical considerations
Note that you will need a paper cutter if you are doing more than one fold.

Note that it is still up to you to figure out how to split up your page signatures if your PDF is not 2^N pages long. For example, if your PDF is 24 pages long, you may be better off doing 3x 8-page signatures than trying to make a one-signature layout. You could also cheat by inserting blank pages in the middle of the input PDF to pad it to 32 pages before layout, and removing those slices after printing and cutting.

## Entry point
```
./mini-page-layout.sh <input pdf> <number of folds>
```

## Examples
To turn a PDF of sequential A7 pages into a print-ready A4 pdf:
```
./mini-page-layout.sh my-zine-A7.pdf 3`
```

To turn a PDF of sequential A6 pages into a print-ready A4 pdf:
```
./mini-page-layout.sh my-other-zine-A6.pdf 2`
```

You can also add the `-l` flag for landscape mode. Otherwise, it will use portrait mode by default.
```
./mini-page-layout.sh -l my-zine-A7.pdf 3
```

## Options
```
-l   set if in landscape mode
-t   test python file but don't compile TeX
-q   quiet output (suppress verbose TeX compilation messages)
```

If you need letter size paper instead of A4: the Python script theoretically supports it, but I didn't enable that option in the bash entry point because I don't have letter size paper at home.

# How it works

The Python script, `mini-page-layout.py`, runs a single iteration of the fold process. It generates and compiles a LaTeX template which arranges your small pages into a layout that, when printed (on paper one size up) and folded, will give you a zine with the pages in the correct order.

The bash entry point, `mini-page-layout.sh`, calls the Python script once for each fold needed, and also does some file management and cleanup.
