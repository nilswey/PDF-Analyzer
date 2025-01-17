from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pdf_analyzer import analyze_pdf, show_keyterms
from wordcloud import WordCloud

# Custom Worker Thread for File Processing
class FileProcessorThread(QThread):
    result_ready = pyqtSignal(dict, str, str)  # Signal to emit results (metadata, lemma_text, error)
    error_occurred = pyqtSignal(str)  # Signal for error messages

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            # Analyze the PDF
            lemma_text, meta = analyze_pdf(self.file_path)
            self.result_ready.emit(meta, lemma_text, None)  # Emit results
        except Exception as e:
            self.result_ready.emit({}, "", str(e))  # Emit an error signal


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
        self.setFixedSize(1400, 700)

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        # Set up User Interface
        self.title = QLabel("PDF Analyzer")  # Top center title
        self.select_text = QLabel("Select PDF File to Analyze:")
        self.select_button = QPushButton("Select File")
        self.clear_button = QPushButton("Clear")
        self.file_path_label = QLabel("No file selected")  # Label to show the selected file path

        # Style Top Row
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

        # Add and apply font style
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

        for label in property_labels:
            label.setFont(font_left_label)

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

        # Connect the buttons to their methods
        self.select_button.clicked.connect(self.select_file)
        self.clear_button.clicked.connect(self.clear_widgets)

    def select_file(self):
        """Handles the file selection process."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        if file_path:
            self.file_path_label.setText("Processing...")
            self.pdf_file_path = file_path
            self.start_file_processing(file_path)

    def start_file_processing(self, file_path):
        """Starts the file processing in a separate thread."""
        self.thread = FileProcessorThread(file_path)
        self.thread.result_ready.connect(self.update_results)
        self.thread.error_occurred.connect(self.show_error)
        self.thread.start()

    def update_results(self, meta, lemma_text, error):
        """Updates the UI with the processed file results."""
        if error:
            self.file_path_label.setText(f"Error: {error}")
            return

        self.pdf_title.setText(meta.get("title", "N/A"))
        self.pdf_author.setText(meta.get("author", "N/A"))
        self.pdf_keywords.setText(meta.get("keywords", "N/A"))
        self.pdf_page_no.setText(str(meta.get("page_no", "N/A")))
        self.word_count.setText(str(meta.get("word_count", "N/A")))
        self.sent_count.setText(str(meta.get("sentence_count", "N/A")))
        self.word_count_unique.setText(str(meta.get("unique_perc", "N/A")))
        self.readability.setText(str(meta.get("read_dif", "N/A")))

        # Generate Word Cloud
        wordcloud = WordCloud(background_color="White", colormap='RdYlGn', max_words=50).generate(lemma_text)
        self.wordcloud.clear()
        ax = self.wordcloud.add_subplot(111)
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        self.wordcloud_canvas.draw()

    def clear_widgets(self):
        """Clears all widgets."""
        self.pdf_title.clear()
        self.pdf_author.clear()
        self.pdf_keywords.clear()
        self.pdf_page_no.clear()
        self.sent_count.clear()
        self.word_count.clear()
        self.word_count_unique.clear()
        self.readability.clear()
        self.file_path_label.setText("No file selected")
        self.wordcloud.clear()
        self.wordcloud_canvas.draw()
        self.keyterms.clear()
        self.keyterms_canvas.draw()


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
