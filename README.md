This script generates zine print layouts that are meant to be folded from letter/A4 paper. I wrote it to streamline the A7 size [zines](https://distractibility.github.io) I sometimes make at home.

Specifically, it expects an input PDF formatted as a page size you would get by folding a sheet N times (e.g. folding an A4 sheet into A5, A6, A7 size).

It then generates a series of LaTeX templates which arrange your small pages into a layout that, when printed and folded up, will give you a zine with the pages in the correct order.

### Environment
```
source venv/bin/activate
```

### Usage
Entry point:
```
./mini-page-layout.sh <input pdf> <number of folds>
```
Under the hood, this bash script calls a python script, `mini-page-layout.py`, which runs a single iteration of the folding process. The python script in turn generates and compiles the LaTeX templates. The bash script calls the python script as many times as folds are needed, and takes care of filesystem dirty work.

### Examples
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

### Options
```
-h, --help         show this help message and exit
--folds=NUM_FOLDS  max folds: 3
--landscape        set if in landscape mode
--a4               set if using A4 paper; default is letter
```

You can see the help message by running `python mini-page-layout.py --help`. However, the Python script only runs a single iteration of the folding process. If your page is folded more than once, you will in practice be using the bash script `mini-page-layout.sh` instead.

