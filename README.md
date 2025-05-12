# Harvest Notebook

Developed by David Blessent

almondhouse27/harvest-notebook

### Requirements

*Python*
[Download Python](https://www.python.org/downloads/)

*Jupyter Notebooks*
```shell
pip install notebook
```

*Pandas*
```shell
pip install pandas
```

*Beautiful Soup*
```shell
pip install beautifulsoup4
```

### Input

To use the *Harvest Notebook* provide a list of URLs in the `data/input/url-list.csv` file.

The program is expecting a single 'url' column in the .csv.

There is also an option `To read URLs directly from code`.

To use this, make sure to comment out the cell `To read URL list from input file`.


### Output

*Harvest Notebook* generates several output files in the `data/output` directory.

`url-analysis.csv` provide general site information about each URL in the input list.

`website-words.csv` provides a word count for each unique word for each URL in the input list.
