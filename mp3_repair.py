import os
import threading
import glob

def repair_file(file_path, repaired_folder_path):
    BYTES_TO_KEEP = 4
    BYTES_TO_ADD = b'\x00' * 12
    REPAIR_SIZE = 334

    with open(file_path, 'rb') as original_file:
        # Read the first 4 bytes
        first_bytes = original_file.read(BYTES_TO_KEEP)
        
        # Read the rest of the file content
        file_content = original_file.read()

        # Remove the last 334 bytes
        repaired_content = file_content[:-REPAIR_SIZE]

        # Construct repaired content by concatenating first bytes, additional bytes, and truncated content
        repaired_content = first_bytes + BYTES_TO_ADD + repaired_content

        # Get the file name without extension
        file_name, file_ext = os.path.splitext(os.path.basename(file_path))

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
        
        print("Processed:", file_path)

def main():
    folder_path = input("Enter the path to the folder containing encrypted MP3 files: ")

    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return

    # Create a "Repaired" folder if it doesn't exist
    repaired_folder_path = os.path.join(folder_path, "Repaired")
    if not os.path.exists(repaired_folder_path):
        os.makedirs(repaired_folder_path)

    # Get list of encrypted MP3 files with proper .mp3 extension
    encrypted_files = glob.glob(os.path.join(folder_path, '*.mp3.*'))

    # Create and start repair threads for each file
    repair_threads = []
    for file_path in encrypted_files:
        repair_thread = threading.Thread(target=repair_file, args=(file_path, repaired_folder_path))
        repair_threads.append(repair_thread)
        repair_thread.start()

    # Wait for all repair threads to finish
    for thread in repair_threads:
        thread.join()

    print("Repair process completed. Repaired files saved to:", repaired_folder_path)

if __name__ == "__main__":
    main()
