# MP3 Repair Tool

This Python application provides a graphical interface for repairing encrypted MP3 files by removing a specific number of bytes from each file.

## Features
- Allows users to select a folder containing encrypted MP3 files for repair.
- Repairs encrypted MP3 files by removing a specified number of bytes from each file.
- Displays progress of the repair process through a progress bar.
- Logs repair progress and status messages in a text box.
- Notifies users upon completion of the repair process.

## Requirements
- Python 3.x
- PyQt6

## Usage
1. Run the script.
2. Browse and select the folder containing the encrypted MP3 files you want to repair.
3. Click the "Repair" button to start the repair process.
4. Progress of the repair process will be displayed in the progress bar.
5. Once the repair process is complete, a message box will inform you of the success and provide the path to the repaired files.

## Instructions
1. Install Python 3.x on your system if not already installed.
2. Install PyQt6 library using pip:
    ```
    pip install PyQt6
    ```
3. Run the script using Python:
    ```
    python mp3repair-gui.py
    ```

## How it Works
- The application scans the selected folder for encrypted MP3 files with the proper extension.
- It reads each file, removes a specific number of bytes from the end, and saves the repaired file in a new folder.
- Progress of the repair process is updated in real-time, and a log of the process is displayed.

## Note
- Make sure to create a backup of your encrypted MP3 files before using this tool, as it modifies the original files.