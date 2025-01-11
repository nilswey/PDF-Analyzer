from functools import partial

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

def analyze_pdf(pdf_file):
    """
    Analyzes a PDF file to extract text, metadata, and perform natural language processing using spaCy and textacy.

    Parameters:
        pdf_file (str): Path to the PDF file.

    Returns:
        tuple: (lemmatized_text, metadata_dict)
    """
    # Load the spaCy NLP model
    nlp = spacy.load("en_core_web_sm")

    # Open the PDF file with PyMuPDF
    with fitz.open(pdf_file) as pdf:
        full_text = ""

        # Extract metadata safely
        pdf_page_no = pdf.page_count
        pdf_title = pdf.metadata.get("title", "Unknown Title")
        pdf_author = pdf.metadata.get("author", "Unknown Author")
        pdf_keywords = pdf.metadata.get("keywords", "No Keywords")

        # Extract text from all pages
        for page in pdf:
            full_text += page.get_text()

        # Word count before cleaning
        words = full_text.replace('\n', ' ').split()
        orig_word_count = len(words)

        # Clean references, appendices, and other unwanted sections
        split_words = ["References", "Appendix", "Appendices", "Footnotes", "Glossary"]
        for word in split_words:
            if word in full_text:
                text_list = full_text.split(word)[:-1]
                # test_split = text.split(word)[-1]
                full_text = " ".join(text_list)  # Keep text before the first occurrence
                break  # Stop after the first match

        # Replace "et al."
        full_text = full_text.replace("et al.", " ")

        # Define Pipeline of things that should be removed or normalized
        preproc = preprocessing.make_pipeline(
            preprocessing.remove.brackets,
            preprocessing.normalize.hyphenated_words,
            preprocessing.normalize.unicode,
            preprocessing.normalize.whitespace,
            preprocessing.normalize.quotation_marks,
            preprocessing.normalize.bullet_points,
            preprocessing.remove.punctuation,
            preprocessing.remove.brackets,
            partial(preprocessing.replace.urls, repl="placeholder_"),
            partial(preprocessing.replace.emails, repl="placeholder_"),
            partial(preprocessing.replace.emojis, repl="placeholder_"),
            partial(preprocessing.replace.hashtags, repl="placeholder_"),
            partial(preprocessing.replace.numbers, repl="placeholder_"),
            partial(preprocessing.replace.phone_numbers, repl="placeholder_"),
            partial(preprocessing.replace.user_handles, repl="placeholder_")
        )

        prep_text = preproc(full_text)
        # clean all the definded placeholder
        prep_text= prep_text.replace("placeholder_", "")


        # Process the text with spaCy
        text_nlp = nlp(prep_text)

        # Extract text statistics using textacy
        sentence_count = text_stats.basics.n_sents(text_nlp)  # Number of sentences
        read_dif = text_stats.readability.flesch_reading_ease(text_nlp)  # Flesch Reading Ease score
        unique_count = text_stats.basics.n_unique_words(text_nlp)  # Number of unique words

        # Lemmatize text and filter out stopwords, punctuation, and spaces
        normalized_text_list = [
            token.lemma_.lower() for token in text_nlp
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        lemmatized_text = " ".join(normalized_text_list)

        # Store metadata results in a dictionary
        Meta = {
            "title": pdf_title,
            "author": pdf_author,
            "keywords": pdf_keywords,
            "page_no": pdf_page_no,
            "word_count": orig_word_count,
            "sentence_count": sentence_count,
            "unique_count": unique_count,
            "read_dif": read_dif,
        }

    return lemmatized_text, Meta


def show_keyterms(text):

    doc = textacy.make_spacy_doc(text, lang="en_core_web_sm")
    # extract keyterms from text that are found in functionally connected words with length of 2,3 or 4, return only top 5 scoring
    sgrank_list = extract.keyterms.sgrank(doc, ngrams=(2, 3, 4), topn=5)


    # extract the items and values from sets in list
    terms = [item[0] for item in sgrank_list]
    values = [item[1] for item in sgrank_list]

    return terms, values


pdf = 'sample.pdf'

lemmatized_text, Meta = analyze_pdf(pdf)

#generate_wordcloud(lemmatized_text)
show_keyterms(lemmatized_text)

#print(lemmatized_text)
#print(Meta)
