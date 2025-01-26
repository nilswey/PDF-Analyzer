import re
import spacy
import fitz  # PyMuPDF
from textacy.preprocessing import remove, normalize, replace
from textacy import text_stats, extract
import time



def get_school_level(score):

    # translate flesch reading score to school levels.
    # based on https://pages.stern.nyu.edu/~wstarbuc/Writing/Flesch.htm

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

    # Start timer
    start_time = time.time()
    nlp = spacy.load("en_core_web_sm")

    # open pdf
    with fitz.open(pdf_file) as pdf:
        full_text = ""

        # get metadata though pymu/fitz
        pdf_page_no = pdf.page_count
        pdf_title = pdf.metadata.get("title", "Unknown Title")
        pdf_author = pdf.metadata.get("author", "Unknown Author")
        pdf_keywords = pdf.metadata.get("keywords", "No Keywords")

        # set up list to contain headers and footers
        page_headers = []
        page_ends = []

        # extract text page by page, add to text
        for page in pdf:
            page_text = page.get_text()
            full_text += page_text

            # Headers and Fotters removal
            # text is split by \n leaving rows of text
            # first and last rows are searched for patterns
            rows = page_text.split("\n")

            first_rows = rows[:4]
            last_rows = rows[-4:]
            page_headers.extend(first_rows)
            page_ends.extend(last_rows)

        print("Text sucessfully extracted")

        # Find duplicate rows in extracted headers/footers
        seen_t = set()
        dupes_t = []

        seen_b = set()
        dupes_b = []


        for row in page_headers:
            if row in seen_t:
                dupes_t.append(row)
            else:
                seen_t.add(row)

        for row in page_ends:
            if row in seen_b:
                dupes_b.append(row)
            else:
                seen_b.add(row)

        # union the duplciates and simplify removal through set
        dupes = set(dupes_t).union(set(dupes_b))

        if len(dupes) < 0:
            for duplicate in dupes:
                full_text = full_text.replace(re.escape(duplicate), "")
            print("Headers and Footers sucessfully removed")


        # get rid of References or Appendix, by splitting text at last occurence of split words
        split_words = ["References", "Appendix", "Appendices", "Glossary"]
        for word in split_words:
            if word in full_text:
                full_text = " ".join(full_text.split(word)[:-1])
                print(f"Removed {word} sucessfully")
                break #break as soon as one is found stop

        # replace words commonly found in scientific papers
        reference_terms = [
            "Figure", "Fig.", "Table", "Tbl.", "Eq.", "Equation", "Exp.",
            "Appendix", "Supplementary Figure", "Supplementary Table",
            "Chart", "Graph", "Panel", "Diagram", "Plot", "et al.", "et al"
        ]

        # Loop through the reference terms and replace them with a space
        for term in reference_terms:
            # Ensure case sensitivity and handle potential punctuation afterwards
            pattern = r"\b" + re.escape(term) + r"\b[:.]?\s?\d*"
            full_text = re.sub(pattern, " ", full_text)

        # use the preprocessing methods from spacy
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
        print("Preproccessing of text sucessfull")

        # get word count, by compiling a list that is split by " "
        orig_word_count = len(full_text.replace('\n', " ").split())

        # apply languague model to the text
        # here each word is analyzed and gets meaning assigned
        full_text = nlp(full_text)
        print("Processing Text via Language Model")

        # extracts leyterms in text
        # simple explanation: https://www.markovml.com/blog/textrank-algorithm
        try:
            sgrank_list = extract.keyterms.textrank(
                full_text,
                topn=5,
                window_size=4,
                normalize="lemma",
                include_pos = "NOUN"
            )
            print("Extracted key terms")

            # return important terms and weights ins seperate lists
            terms = [item[0] for item in sgrank_list]
            values = [item[1] for item in sgrank_list]


        except Exception as e:
            print(f"Error in keyword extraction: {e}")
            return [], []


        # get additional metadata from text
        sentence_count = text_stats.basics.n_sents(full_text)
        read_dif = text_stats.readability.flesch_reading_ease(full_text)
        unique_count = text_stats.basics.n_unique_words(full_text)

        # assign meaning to reading index
        reading_lvl = get_school_level(read_dif)
        print("Calculated Metadata")

        # processesed text is brought into lemma (Grundform), is lowered
        # fill words and punctuation is removed for word
        normalized_text_list = [
            token.lemma_.lower() for token in  full_text
            if not token.is_stop and not token.is_punct and not token.is_space
        ]

        # text goes back from spacy Doc Format to Text
        lemmatized_text = " ".join(normalized_text_list)
        print("Normalized Text sucessfully")

        # calc percentage of unique words
        unique_perc = f"{round(unique_count / orig_word_count * 100, 2)} %"

        # compile pdf-metadata into list
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

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"PDF Analysis took {elapsed_time:.2f} seconds to execute.")

    return lemmatized_text, Meta , terms, values


