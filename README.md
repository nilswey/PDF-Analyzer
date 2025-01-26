


# PDF Analyzer

## Overview
This programm is designed to analyze english scientific papers in PDF file format and provides
basic overview of the text. 

For installation follow the comands below.

Features:
Metadata on Author, Title, Keywords
Number of Words, Sentences
Information on readability
Overview of the most used words in form of a Wordcloud
extraction of Keyterms used in the PDF


It can also analyze any other form of PDF, but the cleaning process of the pdf is optimized
for scientific papers. Additionally you should be aware to select english papers as the input for the text analysis.
The tool is also not optimized for scanned documents that have been converted to PDF.

## Prerequisites
- Python 3.12
- Git

## Setup Instructions

### 1. Clone the repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/nilswey/PDF-Analyzer.git
```
```bash
cd PDF-Analyzer
```


### 2 Create a virtual environment:

#### Windows Users:
```bash
python -m venv PDF-Analyzer
```
#### Linux/MacOS:
```bash
python3 -m venv PDF-Analyzer
```

### 3 Activate the virtual environment:
#### Windows Users:

```bash
PDF-Analzyer\Scripts\activate

```
#### Linux/MacOS:

```bash
source PDF-Analzyer\Scripts\activate
```

### 4: Install Required Python Packages
With the virtual environment activated, install the project dependencies:
```bash
pip install -r requirements.txt
```
Additionally to the required packages you also have to download the natural processing model that spacy uses
for analyzing text.

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the script

```bash
python main.py
```

