This script generates zine print layouts that are meant to be folded from A4 paper. I wrote it to streamline the A7 size [zines](https://distractibility.github.io) I sometimes make at home.

Specifically, it expects an input PDF formatted as a page size you would get by folding a sheet N times (e.g. folding an A4 sheet into A5, A6, A7 size).

If you need letter size paper instead: the Python script theoretically supports it, but I didn't enable that option in the bash entry point because I don't have letter size paper at home.

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
-q   quiet output of TeX compilation (suppress verbose output)
```

# How it works

The Python script, `mini-page-layout.py`, runs a single iteration of the fold process. It generates and compiles a LaTeX template which arranges your small pages into a layout that, when printed (on paper one size up) and folded, will give you a zine with the pages in the correct order.

The bash entry point, `mini-page-layout.sh`, calls the Python script once for each fold needed, and also does some file management and cleanup.
