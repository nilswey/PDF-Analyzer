from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # initialize fields needed for displaying results later
        self.pdf_file_path = None

        # properties for left column
        self.pdf_title = None
        self.pdf_author = None
        self.pdf_keywords = None
        self.pdf_page_no = None
        self.sent_count = None
        self.word_count = None
        self.word_count_unique = None
        self.readability = None

        # create objects for right side
        self.wordcloud = plt.figure()
        self.wordcloud_canvas = FigureCanvas(self.wordcloud)

        self.figure_right = plt.figure()
        self.figure_right_canvas = FigureCanvas(self.figure_right)


        # Configure the main window
        self.setWindowTitle("PDF Analyzer")
        self.resize(1200, 700)

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        """Sets up the user interface."""

        # Create all widgets
        self.title = QLabel("PDF Analyzer")  # Top center title
        self.select_text = QLabel("Select PDF File to Analyze:")
        self.select_button = QPushButton("Select File")
        self.file_path_label = QLabel("No file selected")  # Label to show the selected file path


        # Create Labels for first Row - Left Col
        self.pdf_title_label = QLabel("PDF Title:")
        self.pdf_author_label = QLabel("PDF Author:")
        self.pdf_keywords_label = QLabel("PDF Keywords:")

        # Create Labels for second Row - Left Col
        self.pdf_page_no_label = QLabel("Number of Pages:")
        self.sent_count_label = QLabel("Sentence Count:")
        self.word_count_label = QLabel("Number of Words:")
        self.word_count_unique_label = QLabel("Number of Unique Words:")

        # Create readability object
        self.readability_label = QLabel("Readability Score:")


        # Placeholders for Analysis resutls

        self.pdf_title = QLabel("PDF Title Place")
        self.pdf_author = QLabel("PDF Author Place")
        self.pdf_keywords = QLabel("PDF Keywords Place")

        # Create Labels for second Row - Left Col
        self.pdf_page_no = QLabel("Number of Pages Place")
        self.sent_count = QLabel("Sentence Count PLace")
        self.word_count = QLabel("Number of Words Place")
        self.word_count_unique = QLabel("Number of Unique Words Place")

        # Create readability object
        self.readability = QLabel("Readability Score Place")

        # create figures for right side
        #self.wordcloud = QLabel("Wordcloud Placeholder")
        #self.figure_right = QLabel("Figure Placeholder")


        # Master layout where everything goes into
        self.master_layout = QVBoxLayout()

        # Create top centered objects in horizontal layout
        self.title_box = QHBoxLayout()

        # Add widgets to title box
        self.title_box.addWidget(self.title)
        self.title_box.addStretch()  # Add stretch to the right
        self.title_box.addWidget(self.select_text)
        self.title_box.addWidget(self.select_button)
        self.title_box.addWidget(self.file_path_label)


        # Create column layouts
        self.bot_row = QHBoxLayout()
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Rows in the left column
        self.left_row1 = QHBoxLayout()
        self.left_row2 = QHBoxLayout()
        self.left_row3 = QHBoxLayout()
        self.left_row4 = QHBoxLayout()
        self.left_row5 = QHBoxLayout()
        self.left_row6 = QHBoxLayout()
        self.left_row7 = QHBoxLayout()
        self.left_row8 = QHBoxLayout()


        # add widgets to left rows and col
        self.left_row1.addWidget(self.pdf_title_label)
        self.left_row2.addWidget(self.pdf_author_label)
        self.left_row3.addWidget(self.pdf_keywords_label)

        self.left_row4.addWidget(self.pdf_page_no_label)
        self.left_row5.addWidget(self.sent_count_label)
        self.left_row6.addWidget(self.word_count_label)
        self.left_row7.addWidget(self.word_count_unique_label)

        self.left_row8.addWidget(self.readability_label)


        # Add Analasys Results
        self.left_row1.addWidget(self.pdf_title)
        self.left_row2.addWidget(self.pdf_author)
        self.left_row3.addWidget(self.pdf_keywords)

        self.left_row4.addWidget(self.pdf_page_no)
        self.left_row5.addWidget(self.sent_count)
        self.left_row6.addWidget(self.word_count)
        self.left_row7.addWidget(self.word_count_unique)

        self.left_row8.addWidget(self.readability)

        # Rows in the right column
        #self.right_row1 = QHBoxLayout()
        #self.right_row2 = QHBoxLayout()


        self.right_column.addWidget(self.wordcloud_canvas)
        self.right_column.addWidget(self.figure_right_canvas)

        # Add rows to columns
        self.left_column.addLayout(self.left_row1)
        self.left_column.addLayout(self.left_row2)
        self.left_column.addLayout(self.left_row3)
        self.left_column.addLayout(self.left_row4)
        self.left_column.addLayout(self.left_row5)
        self.left_column.addLayout(self.left_row6)
        self.left_column.addLayout(self.left_row7)
        self.left_column.addLayout(self.left_row8)


        # Add layouts to master layout

        self.bot_row.addLayout(self.left_column, 40)
        self.bot_row.addLayout(self.right_column, 60)
        self.master_layout.addLayout(self.title_box, 5)
        self.master_layout.addLayout(self.bot_row, 95)

        # Set the main layout for the window
        self.setLayout(self.master_layout)

        # Connect the button to the file selection method
        self.select_button.clicked.connect(self.select_file)

    def select_file(self):
        """Handles the file selection process."""
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        # Check if a file was selected
        if file_path:
            # Update the label with the selected file path
            self.file_path_label.setText(file_path)
            self.pdf_file_path = file_path

            # You can add functionality to "do something" with the file here
            self.process_file(file_path)
        else:
            self.file_path_label.setText("No file selected")

    def process_file(self, file_path):


        print(f"Processing file: {file_path}")
        # Add your processing code here, such as analyzing the PDF file


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
