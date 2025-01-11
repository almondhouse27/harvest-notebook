
<!--=== === === === === === === === === -->

<div><img src="src/assets/harvest-notebook.png" alt="Harvest Notebook logo by David Blessent" width="822"/></div>

<!--=== === === === === === === === === -->

# Harvest Notebook (v0.1)

* *Developed by: David Blessent*
* *Published by: Almond House Publishing, LLC.*
* *Available at: https://github.com/almondhouse27/harvest-notebook*


<!--=== === === === === === === === === -->

## Description

A modular and interactive web scraper designed for flexibility and scalability, *Harvest Notebook* allows users to input a list of URLs, check robots.txt files for permissions, scrape data from websites, and generate a suite of comprehensive reports with the click of a button. Reports include page specifications, extracted data, and diagnostics of the scraping process. Built with a *Jupyter Notebook* interface for user interactivity and *Python* libraries for robust core functionality and analytics.

<!--=== === === === === === === === === -->

## Requirements

The following are required to run *Harvest Notebook*:

* *Jupyter Notebooks*
* *Python >= 3.12*
* *Python Libraries\**

\*The *Python* libraries required are specified in `requirements.txt`. 

Note: There is a cell in the 'Notebook Setup' section of *Harvest Notebook* that calls the `install_requirements()` function from the `config.py` file. That functions handles the installation of the required libraries.

### Install Python and Jupyter

1. Install Python 

To run *Harvest Notebook*, you'll need *Python* version 3.12 or higher. Download *Python* from the official site here: https://www.python.org/downloads/

2. Install Jupyter 

After installing *Python*, *Jupyter* can be installed via `pip`, *Python's* package manager. Open a terminal or command prompt and run the following command:

- `pip install jupyter`

Alternatively, *Jupyter* is included in the *Anaconda* distribution, which is a popular *Python* distribution for data science. You can download *Anaconda* here: https://www.anaconda.com/download

### Recommended IDEs

To work with *Harvest Notebook*, you'll need an integrated development environment (IDE) to run the *Jupyter Notebooks*. This application was developed in Visual Studio Code. Here are a few IDE suggestions to get you started:

1. Visual Studio Code (VS Code)

A lightweight, powerful IDE for Python development. You can install the Python extension to enable Jupyter notebook support. Download: https://code.visualstudio.com/

2. PyCharm

A popular IDE for Python, with a full feature set and excellent Jupyter notebook support. Download: https://www.jetbrains.com/pycharm/ 

3. JupyterLab

An IDE specifically for Jupyter Notebooks, offering an enhanced interface over the standard Jupyter Notebook. Download: https://jupyter.org/install

<!--=== === === === === === === === === -->

## How To Use Harvest Notebook

*Harvest Notebook* offers a seamless approach to web scraping by combining the power of *Jupyter Notebooks* with modular *Python* code. It’s designed to cater to users of all technical levels, from those simply seeking quick results to developers looking to customize and extend its functionality.

### Modular Design With Python

The core functionality of the program revolves around six custom modules, each handling a distinct aspect of the workflow:

* *Config: Manages configuration settings, including installing required dependencies*
* *Reader: Validates and processes user input data*
* *Cleaner: Processes and formats data for optimal use*
* *Permissions: Interacts with robots.txt files to respect web scraping permissions*
* *Scraper: Extracts content from URLs*
* *Output: Formats and writes data to structured files*
* *Diagnostic: Summarizes runtime metrics and generates diagnostic logs*

### Workflow Overview

1. Input Validation

-> Users start by populating `./data/input/data.csv` with their URLs to scrape. The file must have exactly three columns: `Category`, `Name`, and `Url`. If the structure is incorrect:

* *A backup of the original data is saved to* `./data/input/bad_data.csv`
* *The program resets* `/data/input/data.csv` *with only the required header row* `Category`, `Name`, `Url`.

!! **`The Url field is mandatory`**

! - To enter rows without a Category or Name, include placeholder commas like `,,https://url.here`.

2. Data Cleaning

-> Once the input data has been validated, the program proceeds to clean and format it to ensure compatibility with the scraping process. The following actions take place:

* *Rows with missing Url values are removed*
* *Empty* `Category` *or* `Name` *fields are updated to* `"Unavailable"`
* *A summary of the cleaned data is displayed for review*

3. Scraping and Report Generation

-> The validated and cleaned input data is passed to the scraper, which processes each URL and generates three distinct reports:

* *Website Words (csv): Contains a frequency count of every word appearing on the scraped web pages*

* *Site Specifications (csv): Captures metadata about each page, such as the number of images, forms, and scripts, as well as details like the meta description and site cookie status*

* *Diagnostic Log (json): Summarizes runtime details from the log file, including errors, warnings, and processing times*

! - These reports are saved in a timestamped folder under `./data/output`, ensuring clear organization for each run of the *Harvest Notebook*.

4. Data Formatting

-> The program applies basic formatting and processing to ensure the Website Words and Site Specifications reports are ready for immediate analysis. For example:

*  *The two .csv files can be joined on the* `Url` *column to create a unified dataset for further insights or visualizations*

### Levels of User Interaction

*Harvest Notebook* is designed to be as flexible as its users need it to be:

* *Quick Results: Users can simply upload their data to* `data.csv` *and click "Run All" to generate reports without modifying any code*
* *Customization: For advanced users, each Jupyter Notebook cell is well-documented, providing clear guidance on what each step accomplishes*
* *Transparency makes it easy to trace the program’s logic or add custom functionality by editing the core modules and notebook and scraper constants*

Whether you want a hands-off experience or complete control over the scraping and processing pipeline, Harvest Notebook adapts to suit your needs.

<!--=== === === === === === === === === -->
