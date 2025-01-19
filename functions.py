from functools import partial
import re
from multiprocessing.reduction import duplicate

import spacy
import fitz  # PyMuPDF
import textacy
from textacy.preprocessing.normalize import bullet_points
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textacy import text_stats, extract, preprocessing

nlp = spacy.load("en_core_web_sm")

def generate_wordcloud(text):
    wordcloud = WordCloud(background_color="White", colormap='RdYlGn', max_words=50).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
def show_keyterms(text):

    doc = textacy.make_spacy_doc(text, lang=nlp)
    # extract keyterms from text that are found in functionally connected words with length of 2,3 or 4, return only top 5 scoring
    sgrank_list = extract.keyterms.sgrank(doc, ngrams=(2, 3, 4), topn=5)


    # extract the items and values from sets in list
    terms = [item[0] for item in sgrank_list]
    values = [item[1] for item in sgrank_list]

    return terms, values

"""
def get_school_level(score):
    #translate flesch reading score to school levels.
    # based on https://pages.stern.nyu.edu/~wstarbuc/Writing/Flesch.htm

    if 90 <= score <= 100:
        return f"This text is very easy to read. It corresponds to 5th grade level."

    elif 80 <= score < 90:
        return f"This text is easy to read. It corresponds to 6th grade level."

    elif 70 <= score < 80:
        return f"This text is fairly easy to read. It corresponds to 7th grade level."

    elif 60 <= score < 70:
        return f"This texts reading difficulty is average. It corresponds to 8th and 9th grade level."

    elif 50 <= score < 60:
        return f"This text is fairly difficult to read. It corresponds to 10th to 12th grade level."

    elif 30 <= score < 50:
        return f"This text is difficult to read. It corresponds to college student level."

    elif 0 <= score < 30:
        return f"This text is very difficult to read. It corresponds to college graduate level."

    else:
        return "Invalid Score!"
"""

def get_school_level(score):
    # Translate Flesch reading score to school levels
    levels = [
        (90, 100, "This text is very easy to read. It corresponds to 5th grade level."),
        (80, 90, "This text is easy to read. It corresponds to 6th grade level."),
        (70, 80, "This text is fairly easy to read. It corresponds to 7th grade level."),
        (60, 70, "This text's reading difficulty is average. It corresponds to 8th-9th grade level."),
        (50, 60, "This text is fairly difficult to read. It corresponds to 10th-12th grade level."),
        (30, 50, "This text is difficult to read. It corresponds to college level."),
        (0, 30, "This text is very difficult to read. It corresponds to college graduate level."),
    ]
    for lower, upper, message in levels:
        if lower <= score < upper:
            return message
        else:
            return "Invalid Score!"

def clean_by_list(text, ip_list, row_number):

    if len(ip_list) == 0:
        print("Something went wrong with the Header Cleaning!")
        return Text

    else:
        if len(list_red[row_number:]) > len(set_red:row_number):
            seen = set()
            dupes = []

            # Find duplicate rows
            for row in list_red:
                if row in seen:
                    dupes.append(row)
                else:
                    seen.add(row)

            # Remove duplicates from the text
            for duplicate in dupes:
                text = re.sub(re.escape(duplicate), " ", text)

        return text


def analyze_pdf(pdf_file):
    """
    Analyzes a PDF file to extract text, metadata, and perform natural language processing using spaCy and textacy.

    Parameters:
        pdf_file (str): Path to the PDF file.

    Returns:
        tuple: (lemmatized_text, metadata_dict)
    """


    # Open the PDF file with PyMuPDF
    with fitz.open(pdf_file) as pdf:
        full_text = ""

        # Extract metadata safely
        pdf_page_no = pdf.page_count
        pdf_title = pdf.metadata.get("title", "Unknown Title")
        pdf_author = pdf.metadata.get("author", "Unknown Author")
        pdf_keywords = pdf.metadata.get("keywords", "No Keywords")

        page_headers = []
        page_ends = []
        # Extract text from all pages
        for page in pdf:
            page_text = page.get_text()

            full_text += page_text

            #extract potential and append to list
            rows = page_text.split("\n")
            # get first two rows in case there is a page number on the left side
            first_rows = rows[0:4]
            last_rows = rows[-4:]
            page_headers.extend(first_rows)
            page_ends.extend(last_rows)

        # make headers a set to remove duplicates
        # first page could be title page thats why it is left out
        header_set = set(page_headers[4:])
        bottom_set = set(page_ends[4:])

        # if the number of items in the header set is smaller there are duplicates
        if len(header_set) < len(page_headers[4:]):
            #if duplicates are found remove all the text found in the first rows because there is a pattern
            dups_t = [row for row in page_headers if row in header_set]
            for row in dups_t:
                full_text = re.sub(re.escape(row)," ", full_text)

        if len(bottom_set) < len(page_ends[4:]):
            dups_b = [row for row in page_ends if row in bottom_set]
            for row in dups_b:
                full_text = re.sub(re.escape(row)," ", full_text)


        # Word count before cleaning
        words = full_text.replace('\n', " ").split()
        orig_word_count = len(words)

        # Clean references, appendices, and other unwanted sections
        split_words = ["References", "Appendix", "Appendices", "Footnotes", "Glossary"]
        for word in split_words:
            if word in full_text:
                text_list = full_text.split(word)[:-1]
                # test_split = text.split(word)[-1]
                full_text = " ".join(text_list)  # Keep text before the first occurrence
                break  # Stop after the first match

        # Replace "et al." found in scientific papers
        full_text = full_text.replace("et al.", " ")

        # Define Pipeline of things that should be removed or normalized
        preproc = preprocessing.make_pipeline(
            preprocessing.remove.brackets,
            preprocessing.normalize.hyphenated_words,
            preprocessing.normalize.unicode,
            preprocessing.normalize.whitespace,
            preprocessing.normalize.quotation_marks,
            preprocessing.normalize.bullet_points,
            partial(preprocessing.replace.urls, repl=" "),
            partial(preprocessing.replace.emails, repl=" "),
            partial(preprocessing.replace.emojis, repl=" "),
            partial(preprocessing.replace.hashtags, repl=" "),
            partial(preprocessing.replace.numbers, repl=" "),
            partial(preprocessing.replace.phone_numbers, repl=" "),
            partial(preprocessing.replace.user_handles, repl=" ")
        )

        prep_text = preproc(full_text)


        # Process the text with spaCy
        text_nlp = nlp(prep_text)

        # Extract text statistics using textacy
        sentence_count = text_stats.basics.n_sents(text_nlp)  # Number of sentences
        read_dif = text_stats.readability.flesch_reading_ease(text_nlp)  # Flesch Reading Ease score
        unique_count = text_stats.basics.n_unique_words(text_nlp)  # Number of unique words


        # assign meaning to Flesch reading score
        reading_lvl = get_school_level(read_dif)


        # Lemmatize text and filter out stopwords, punctuation, and spaces
        normalized_text_list = [
            token.lemma_.lower() for token in text_nlp
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        lemmatized_text = " ".join(normalized_text_list)

        unique_perc = str(round(unique_count/orig_word_count *100, 2)) + "%"

        # Store metadata results in a dictionary
        Meta = {
            "title": pdf_title,
            "author": pdf_author,
            "keywords": pdf_keywords,
            "page_no": pdf_page_no,
            "word_count": orig_word_count,
            "sentence_count": sentence_count,
            "unique_perc": unique_perc,
            "read_dif": reading_lvl
        }

    return lemmatized_text, Meta,




"""
#pdf = 'sample.pdf'

#lemmatized_text, Meta = analyze_pdf(pdf)

#generate_wordcloud(lemmatized_text)
#show_keyterms(lemmatized_text)

#print(lemmatized_text)
#print(Meta)
"""