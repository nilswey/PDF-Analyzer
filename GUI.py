import tkinter as tk
from tkinter import filedialog, Label, Button, Text, Scrollbar, END, Toplevel
from tkinter import messagebox


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Analysis Tool")
        self.root.geometry("500x300")

        # Instructions label
        self.instructions = Label(self.root, text="Select a PDF file to analyze:", font=("Arial", 12))
        self.instructions.pack(pady=10)

        # File selection button
        self.select_button = Button(self.root, text="Select File", command=self.select_file, font=("Arial", 10))
        self.select_button.pack(pady=5)

        # File path label
        self.file_path_label = Label(self.root, text="No file selected", font=("Arial", 10), wraplength=400)
        self.file_path_label.pack(pady=5)

        # Analyze button (disabled by default)
        self.analyze_button = Button(self.root, text="Analyze File", command=self.analyze_file, font=("Arial", 10), state=tk.DISABLED)
        self.analyze_button.pack(pady=20)

    def select_file(self):
        """Handle file selection."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path_label.config(text=file_path)
            self.analyze_button.config(state=tk.NORMAL)  # Enable the Analyze button
        else:
            self.file_path_label.config(text="No file selected")
            self.analyze_button.config(state=tk.DISABLED)  # Disable the Analyze button

    def analyze_file(self):
        """Analyze the selected file."""
        file_path = self.file_path_label.cget("text")
        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select a file first.")
            return

        # Call your PDF analysis function here
        # For now, we'll just display a message
        analysis_result = f"Analysis for file: {file_path}\n\n[Add your analysis code here]"
        self.show_results_window(analysis_result)

    def show_results_window(self, analysis_result):
        """Display analysis results in a new window."""
        results_window = Toplevel(self.root)
        results_window.title("Analysis Results")
        results_window.geometry("600x400")

        # Text widget for displaying results
        results_text = Text(results_window, wrap="word")
        results_text.insert(END, analysis_result)
        results_text.config(state="disabled")  # Make the text read-only
        results_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Add a scrollbar
        scrollbar = Scrollbar(results_text)
        scrollbar.pack(side="right", fill="y")
        results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=results_text.yview)

    def on_close(self):
        """Handle the closing event of the application."""
        # Play the Windows XP shutdown sound in a separate thread
        sound_path = "/music/windowsxp.mp3"  # Update with your sound file path
        threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()

        # Close the app after the sound is played
        self.root.after(2000, self.root.destroy)  # Adjust delay (in ms) based on the sound length

# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
