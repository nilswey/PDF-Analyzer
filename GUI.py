from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from functions import analyze_pdf, generate_wordcloud, show_keyterms
from wordcloud import WordCloud

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize fields needed for displaying results later
        self.pdf_file_path = None

        # Properties for left column
        self.pdf_title = QLabel("")
        self.pdf_author = QLabel("")
        self.pdf_keywords = QLabel("")
        self.pdf_page_no = QLabel("")
        self.sent_count = QLabel("")
        self.word_count = QLabel("")
        self.word_count_unique = QLabel("")
        self.readability = QLabel("")

        # Create objects for the right side
        self.wordcloud = plt.figure()
        self.wordcloud_canvas = FigureCanvas(self.wordcloud)

        self.keyterms = plt.figure()
        self.keyterms_canvas = FigureCanvas(self.keyterms)

        # Configure the main window
        self.setWindowTitle("PDF Analyzer")
        self.resize(1400, 700)

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        # Set up User Interface
        # Create all widgets
        self.title = QLabel("PDF Analyzer")  # Top center title
        self.select_text = QLabel("Select PDF File to Analyze:")
        self.select_button = QPushButton("Select File")
        self.clear_button = QPushButton("Clear")
        self.file_path_label = QLabel("No file selected")  # Label to show the selected file path

        #Style Top Row:
        font_title = QFont("Helvetica Neue", 18)
        font_title.setBold(True)
        self.title.setFont(font_title)
        font_select = QFont("Helvetica Neue", 10)

        self.select_text.setFont(font_select)
        self.select_button.setFont(font_select)
        self.clear_button.setFont(font_select)

        # Master layout where everything goes into
        self.master_layout = QVBoxLayout()

        # Create top centered objects in horizontal layout
        self.title_box = QHBoxLayout()

        # Add widgets to title box
        self.title_box.addWidget(self.title)
        self.title_box.addStretch()  # Add stretch to the right
        self.title_box.addWidget(self.select_text)
        self.title_box.addWidget(self.select_button)
        self.title_box.addWidget(self.clear_button)
        self.title_box.addWidget(self.file_path_label)

        # Create column layouts under title box
        self.bot_row = QHBoxLayout()
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Create labels in the left column
        pdf_title_label = QLabel("PDF Title:")
        pdf_author_label = QLabel("PDF Author:")
        pdf_keywords_label = QLabel("PDF Keywords:")
        pdf_page_no_label = QLabel("Number of Pages:")
        sent_count_label = QLabel("Sentence Count:")
        word_count_label = QLabel("Number of Words:")
        word_count_unique_label = QLabel("Percentage of Unique Words:")
        readability_label = QLabel("Readability:")

        # add and apply font style
        font_left_label = QFont("Helvetica Neue", 10)
        font_left_label.setBold(True)



        property_labels = [
            pdf_title_label,
            pdf_author_label,
            pdf_keywords_label,
            pdf_page_no_label,
            sent_count_label,
            word_count_label,
            word_count_unique_label,
            readability_label
        ]

        # Set the font for each label
        for label in property_labels:
            label.setFont(font_left_label)

        # define and apply style to properties
        font_left_property = QFont("Helvetica Neue", 10)

        property_widgets = [
            self.pdf_title,
            self.pdf_author,
            self.pdf_keywords,
            self.pdf_page_no,
            self.sent_count,
            self.word_count,
            self.word_count_unique,
            self.readability,
        ]

        for widget in property_widgets:
            widget.setFont(font_left_property)

        # Add labels and widgets to the left column
        self.left_column.addWidget(pdf_title_label)
        self.left_column.addWidget(self.pdf_title)
        self.left_column.addWidget(pdf_author_label)
        self.left_column.addWidget(self.pdf_author)
        self.left_column.addWidget(pdf_keywords_label)
        self.left_column.addWidget(self.pdf_keywords)
        self.left_column.addWidget(pdf_page_no_label)
        self.left_column.addWidget(self.pdf_page_no)
        self.left_column.addWidget(sent_count_label)
        self.left_column.addWidget(self.sent_count)
        self.left_column.addWidget(word_count_label)
        self.left_column.addWidget(self.word_count)
        self.left_column.addWidget(word_count_unique_label)
        self.left_column.addWidget(self.word_count_unique)
        self.left_column.addWidget(readability_label)
        self.left_column.addWidget(self.readability)

        # Add widgets to right column
        self.right_column.addWidget(self.wordcloud_canvas)
        self.right_column.addWidget(self.keyterms_canvas)


        # Add layouts to master layout
        self.bot_row.addLayout(self.left_column, 40)
        self.bot_row.addLayout(self.right_column, 60)
        self.master_layout.addLayout(self.title_box, 5)
        self.master_layout.addLayout(self.bot_row, 95)

        # Set the main layout for the window
        self.setLayout(self.master_layout)

        # Connect the button to the file selection method
        self.select_button.clicked.connect(self.select_file)
        self.clear_button.clicked.connect(self.clear_widgets)

    def select_file(self):
        """Handles the file selection process."""
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        # Check if a file was selected
        if file_path:
            # Update the label with the selected file path
            self.file_path_label.setText(file_path)
            self.pdf_file_path = file_path

            # Process the selected file
            self.process_file(file_path)
        else:
            self.file_path_label.setText("No file selected")

    def clear_widgets(self):



        property_widgets = [
            self.pdf_title,
            self.pdf_author,
            self.pdf_keywords,
            self.pdf_page_no,
            self.sent_count,
            self.word_count,
            self.word_count_unique,
            self.readability,
            self.wordcloud,
            self.keyterms,
            self.file_path_label
        ]

        for widget in property_widgets:
            widget.clear()

        self.keyterms_canvas.draw()
        self.wordcloud_canvas.draw()

    def process_file(self, file_path):
        """Processes the selected PDF file."""
        try:
            # Analyze the PDF
            lemma_text, meta = analyze_pdf(file_path)

            # Update the labels with metadata
            self.pdf_title.setText(meta["title"])
            self.pdf_author.setText(meta["author"])
            self.pdf_keywords.setText(meta["keywords"])
            self.pdf_page_no.setText(str(meta["page_no"]))
            self.word_count.setText(str(meta["word_count"]))
            self.sent_count.setText(str(meta["sentence_count"]))
            self.word_count_unique.setText(str(meta["unique_perc"]))
            self.readability.setText(str(meta["read_dif"]))

            # Generate the word cloud

            wordcloud = WordCloud(background_color="White", colormap='RdYlGn', max_words=50).generate(lemma_text)
            self.wordcloud.clear()
            ax = self.wordcloud.add_subplot(111)
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            self.wordcloud_canvas.draw()

            # generate keytermns
            terms, values = show_keyterms(lemma_text)
            ax = self.keyterms.add_subplot(111)  # Add a subplot to the keyterms figure

            # Create the bar chart
            barplot = ax.barh(terms, values, color='skyblue')

            # Annotate bars with keywords
            for bar, term in zip(barplot, terms):
                ax.text(
                    bar.get_width() / 2,  # x-coordinate (center of the bar)
                    bar.get_y() + bar.get_height() / 2,  # y-coordinate (center of the bar)
                    term,  # Text to display
                    ha='center', va='center', color='black', fontsize=10, wrap=True
                )

            # Add labels and title
            ax.set_xlabel('Ranked Importance')
            ax.axis("off")  # Hide y-ticks
            ax.set_title('Key Terms')
            ax.invert_yaxis()  # Invert y-axis to display highest score at the top

            # Redraw the canvas
            self.keyterms_canvas.draw()

        except Exception as e:
            print(f"Error processing file: {e}")
            self.file_path_label.setText("Error processing file")


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
