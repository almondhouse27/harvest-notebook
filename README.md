# Harvest Notebook

Developed by David Blessent

almondhouse27/harvest-notebook

## Requirements

**Python**

[Python 3 Documentation](https://docs.python.org/3/)

[python.org/downloads](https://www.python.org/downloads/)

**Platform**

[Jupyter Documentation](https://docs.jupyter.org/en/latest/)

```shell
pip install notebook
```

**Libraries**

[Pandas Documentation](https://pandas.pydata.org/docs/)

```shell
pip install pandas
```

[Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

```shell
pip install beautifulsoup4
```

## Input

To use the *Harvest Notebook* provide a list of URLs in the `data/input/url-list.csv` file.

The program is expecting a single 'url' column in the .csv.

There is also an option `To read URLs directly from code`.

To use this, make sure to comment out the cell `To read URL list from input file`.

## Output

*Harvest Notebook* generates several output files in the `data/output` directory.

`url-analysis.csv` provide general site information about each URL in the input list.

`website-words.csv` provides a word count for each unique word for each URL in the input list.
