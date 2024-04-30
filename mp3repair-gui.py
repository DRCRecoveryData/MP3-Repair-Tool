import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import glob

class MP3RepairWorker(QThread):
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    repair_finished = pyqtSignal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        self.repair_files()

    def repair_files(self):
        BYTES_TO_KEEP = 4
        BYTES_TO_ADD = b'\x00' * 12
        REPAIR_SIZE = 334

        # Create a "Repaired" folder if it doesn't exist
        repaired_folder_path = os.path.join(self.folder_path, "Repaired")
        if not os.path.exists(repaired_folder_path):
            os.makedirs(repaired_folder_path)

        # Get list of encrypted MP3 files with proper .mp3 extension
        encrypted_files = glob.glob(os.path.join(self.folder_path, '*.mp3.*'))

        total_files = len(encrypted_files)
        processed_files = 0

        for file_path in encrypted_files:
            # Get the file name without extension
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            self.log_updated.emit(f"Processing {file_name}...")

            with open(file_path, 'rb') as original_file:
                # Read the first 4 bytes
                first_bytes = original_file.read(BYTES_TO_KEEP)
                
                # Read the rest of the file content
                file_content = original_file.read()

                # Remove the last 334 bytes
                repaired_content = file_content[:-REPAIR_SIZE]

                # Construct repaired content by concatenating first bytes, additional bytes, and truncated content
                repaired_content = first_bytes + BYTES_TO_ADD + repaired_content

                # Check if the extension is not .mp3, keep iterating to find the correct extension
                while file_ext.lower() != ".mp3":
                    # If there's no extension left, break the loop
                    if not file_ext:
                        break
                    # Remove the current extension and check the next one
                    file_name, file_ext = os.path.splitext(file_name)

                # Write the repaired content to the new file in the specified folder
                repaired_file_path = os.path.join(repaired_folder_path, file_name + ".mp3")
                with open(repaired_file_path, 'wb') as repaired_file:
                    repaired_file.write(repaired_content)
                
                processed_files += 1
                progress = int(processed_files / total_files * 100)
                self.progress_updated.emit(progress)
                self.log_updated.emit(f"{file_name} repaired.")

        self.repair_finished.emit(f"Repair process completed. Repaired files saved to: {repaired_folder_path}")

class MP3RepairApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP3 Repair Tool")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.folder_label = QLabel("Encrypted Folder:")
        self.folder_path_edit = QLineEdit()
        self.folder_browse_button = QPushButton("Browse", self)
        self.folder_browse_button.setObjectName("browseButton")
        self.folder_browse_button.clicked.connect(self.browse_folder)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.repair_button = QPushButton("Repair", self)
        self.repair_button.setObjectName("blueButton")
        self.repair_button.clicked.connect(self.repair_mp3_files)

        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_path_edit)
        layout.addWidget(self.folder_browse_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_box)
        layout.addWidget(self.repair_button)

        self.setLayout(layout)

        self.setStyleSheet("""
        #browseButton, #blueButton {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 4px;
        }
        #browseButton:hover, #blueButton:hover {
            background-color: #2980b9;
        }
        """)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path_edit.setText(folder_path)

    def repair_mp3_files(self):
        folder_path = self.folder_path_edit.text()

        if not os.path.exists(folder_path):
            self.show_message("Error", "Folder path does not exist.")
            return

        # Create the MP3 repair worker and start the repair process
        self.worker = MP3RepairWorker(folder_path)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_updated.connect(self.update_log)
        self.worker.repair_finished.connect(self.repair_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_log(self, message):
        self.log_box.append(message)

    def repair_finished(self, message):
        self.show_message("Success", message)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MP3RepairApp()
    window.show()
    sys.exit(app.exec())
