import matplotlib.pyplot as plt
from pymupdf import pymupdf
from wordcloud import WordCloud


def get_pdf_meta(doc):  # has to be NLP
    page_count = doc.page_count
    metadata = doc.metadata
    pdf_author = metadata["author"]
    pdf_title = metadata["title"]
    pdf_keywords = metadata["keywords"]
    word_count = text_stats.basics.n_words(doc)
    sentence_count = text_stats.basics.n_sents(doc)
    unique_count = text_stats.basics.n_unique_words(doc)

    read_dif = text_stats.readability.flesch_reading_ease(doc)
    # Calculate the percentage of unique words
    unique_per = round((unique_count / word_count) * 100, 2)

    # Create a dictionary with variable names as keys and their corresponding values
    result = {
        "page_count": page_count,
        "pdf_author": pdf_author,
        "pdf_title": pdf_title,
        "pdf_keywords": pdf_keywords,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "unique_count": unique_count,
        "unique_per": unique_per
        "read_dif" : read_dif
    }

    return result


def clean_pdf(pdf):
    try:
        with pymupdf.open(pdf) as doc:  # open document
            # get all pages into string
            text = " ".join([page.get_text() for page in doc])
            text = text.replace('\n', ' ')
            text = text.replace('et al', ' ')

            # cleaning references, by removing everything after last occurence of split words
            split_words = ["References", "Appendix", "Appendices", "Footnotes", "Glossary"]

            for word in split_words:
                if word in text:
                    text_list = text.split(word)[:-1]
                    # test_split = text.split(word)[-1]
                    text = " ".join(text_list)

    return text


def normalize_lemma(doc):
    normalized_text_list = []
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_space:
            normalized_text_list.append(token.lemma_.lower())
            normalized_text = ' '.join(normalized_text_list)

            return normalized_text


def generate_wordcloud(text):

    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.show()




def analyze_pdf(pdf_file):
    nlp = spacy.load("en_core_web_sm")

    # open pdf with fitz
    with fitz.open(pdf_file) as pdf:
        full_text = ""

        # update properties that can be extracted via fitz/pymupdf
        pdf_page_no = pdf.page_count
        pdf_title = pdf.metdata["title"]
        pdf_author = pdf.metadata["author"]
        pdf_keywords = pdf.metadata["keywords"]
        pdf_author =  pdf.metadata["author"]


        for page in pdf:
            full_text += page.getText()

        words = full_text.replace('\n', ' ').split()
        self.word_count = len(words)

        # cleaning references, appendices by removing everything after last occurence of split words
        split_words = ["References", "Appendix", "Appendices", "Footnotes", "Glossary"]

        for header in split_words:
            if header in words:
                text_list = words.split(word)[:-1]
                text = " ".join(text_list)
                text = text.replace('et al.', ' ')

            else:
                text = words.replace('et al.', ' ')


        # start natural languague processing of pdf_text
        text_nlp = nlp(text)

        lemma = normalize_lemma(text_nlp)


