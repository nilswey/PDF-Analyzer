from functools import partial
import re
import spacy
import fitz  # PyMuPDF
from textacy.preprocessing import remove, normalize, replace
from textacy import text_stats, extract
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")


def show_keyterms(nlp_text):
    doc = nlp(text)
    sgrank_list = extract.keyterms.sgrank(doc, ngrams=(2, 3, 4), topn=5)
    terms = [item[0] for item in sgrank_list]
    values = [item[1] for item in sgrank_list]
    return terms, values


def get_school_level(score):
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
    return "Invalid Score!"


def analyze_pdf(pdf_file):

    #Analyzes a PDF file to extract text, metadata,
    #performs natural language processing using spaCy and textacy.

    # open pdf
    with fitz.open(pdf_file) as pdf:
        full_text = ""

        # get metadata though pymu/fitz
        pdf_page_no = pdf.page_count
        pdf_title = pdf.metadata.get("title", "Unknown Title")
        pdf_author = pdf.metadata.get("author", "Unknown Author")
        pdf_keywords = pdf.metadata.get("keywords", "No Keywords")

        page_headers = []
        page_ends = []

        # extract text page by page, add to text
        for page in pdf:
            page_text = page.get_text()
            full_text += page_text

            rows = page_text.split("\n")
            first_rows = rows[:4]
            last_rows = rows[-4:]
            page_headers.extend(first_rows)
            page_ends.extend(last_rows)

        header_set = set(page_headers[4:])
        bottom_set = set(page_ends[4:])

        """
        if len(header_set) < len(page_headers[4:]):
            duplicates = [row for row in page_headers if row in header_set]
            for row in duplicates:
                full_text = re.sub(re.escape(row), " ", full_text)

        if len(bottom_set) < len(page_ends[4:]):
            duplicates = [row for row in page_ends if row in bottom_set]
            for row in duplicates:
                full_text = re.sub(re.escape(row), " ", full_text)
        """

        # get word count, by compiling a list that is split by " "
        orig_word_count = len(full_text.replace('\n', " ").split()) 


        # get rid of References or Appendix, by splitting text at last occurence of split words
        split_words = ["References", "Appendix", "Appendices", "Glossary"]
        for word in split_words:
            if word in full_text:
                full_text = " ".join(full_text.split(word)[:-1])
                break

        # replace words commonly found in scientific papers

        # List of common reference terms to look for
        reference_terms = [
            "Figure", "Fig.", "Table", "Tbl.", "Eq.", "Equation", "Exp.",
            "Appendix", "Supplementary Figure", "Supplementary Table",
            "Chart", "Graph", "Panel", "Diagram", "Plot", "et al."
        ]

        # Loop through the reference terms and replace them with a space
        for term in reference_terms:
            # Ensure case sensitivity and handle optional punctuation (colon or period)
            pattern = r"\b" + re.escape(term) + r"\b[:.]?\s?\d*"
            text = re.sub(pattern, " ", text)

        # use the preprocessing methods from spacy,
        # for memeory optimization they all overwrite "full_text"
        full_text = remove.brackets(full_text)
        full_text = normalize.hyphenated_words(full_text)
        full_text = normalize.unicode(full_text)
        full_text = normalize.whitespace(full_text)
        full_text = normalize.quotation_marks(full_text)
        full_text = normalize.bullet_points(full_text)
        full_text = replace.urls(full_text, repl=" ")
        full_text = replace.emails(full_text, repl=" ")
        full_text = replace.emojis(full_text, repl=" ")
        full_text = replace.hashtags(full_text, repl=" ")
        full_text = replace.numbers(full_text, repl=" ")
        full_text = replace.phone_numbers(full_text, repl=" ")
        full_text = replace.user_handles(full_text, repl=" ")

        # apply languague model to the text
        # here each word is analized and gets meaning assigned
        full_text = nlp(full_text)


        sgrank_list = extract.keyterms.sgrank(full_text, ngrams=(2, 3, 4), topn=5)
        terms = [item[0] for item in sgrank_list]
        values = [item[1] for item in sgrank_list]


        # get additional metadata from text
        sentence_count = text_stats.basics.n_sents(full_text)
        read_dif = text_stats.readability.flesch_reading_ease(full_text)
        unique_count = text_stats.basics.n_unique_words(full_text)

        # assign meaning to reading index
        reading_lvl = get_school_level(read_dif)

        # processesed text is brought into lemma (Grundform), is lowered
        # fill words and punctuation is removed for word
        normalized_text_list = [
            token.lemma_.lower() for token in  full_text
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        lemmatized_text = " ".join(normalized_text_list)

        unique_perc = f"{round(unique_count / orig_word_count * 100, 2)}%"

        Meta = {
            "title": pdf_title,
            "author": pdf_author,
            "keywords": pdf_keywords,
            "page_no": pdf_page_no,
            "word_count": orig_word_count,
            "sentence_count": sentence_count,
            "unique_perc": unique_perc,
            "read_dif": reading_lvl,
        }

    return lemmatized_text, Meta, terms, values
