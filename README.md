

This README provides instructions on how to start, connect to, and stop the Docker container for the PDF Analyzer Project.

## 1: Clone the repository:


Navigate to the repository:

cd PDF


# PDF Analyzer

## Overview
This programm is designed to analyze scientific papers in PDF file format and provides
basic overview of the text.

Features:
Metadata on Author, Title, Keywords
Number of Words, Sentences
Information on readability
Overview of the most used words in form of a Wordcloud
extraction of Keyterms used in the PDF

## Prerequisites
- Python 3.12
- Git

## Setup Instructions

### 1. Clone the repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourproject.git
```
```bash
cd pdf-analyzer
```


### 2 Create a virtual environment:

#### Windows Users:
```bash
python -m venv pdf-analyzer
```
#### Linux/MacOS:
```bash
python3 -m venv pdf-analyzer
```

### 3 Activate the virtual environment:
#### Windows Users:

```bash
venv\Scripts\activate.bat
```
#### Linux/MacOS:

```bash
source venv/bin/activate
```

### 4: Install Required Python Packages
With the virtual environment activated, install the project dependencies:
```bash
pip install -r requirements.txt
```

### 5. Run the script

```bash
python main.py
```

