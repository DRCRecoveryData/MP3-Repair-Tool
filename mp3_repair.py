import os
import threading

def repair_file(file_name, repaired_file_path):
    BYTES_TO_KEEP = 4
    BYTES_TO_ADD = b'\x00' * 12
    REPAIR_SIZE = 334

    with open(file_name, 'rb') as original_file:
        # Read the first 4 bytes
        first_bytes = original_file.read(BYTES_TO_KEEP)
        
        # Read the rest of the file content
        file_content = original_file.read()

        # Remove the last 334 bytes
        repaired_content = file_content[:-REPAIR_SIZE]

        # Construct repaired content by concatenating first bytes, additional bytes, and truncated content
        repaired_content = first_bytes + BYTES_TO_ADD + repaired_content

        # Write the repaired content to the new file
        with open(repaired_file_path, 'wb') as repaired_file:
            repaired_file.write(repaired_content)

def main():
    file_name = input("Enter the path to the encrypted MP3 file: ")

    # Remove additional extensions from the file name
    file_name_base, file_extension = os.path.splitext(file_name)
    while file_extension != ".mp3":
        file_name_base, file_extension = os.path.splitext(file_name_base)

    # Construct the repaired file name
    repaired_file_name = os.path.basename(file_name_base) + ".mp3"
    repaired_file_path = os.path.join("Repaired", repaired_file_name)

    # Create a "Repaired" folder if it doesn't exist
    if not os.path.exists("Repaired"):
        os.makedirs("Repaired")

    # Create and start the repair thread
    repair_thread = threading.Thread(target=repair_file, args=(file_name, repaired_file_path))
    repair_thread.start()

    repair_thread.join()  # Wait for the repair thread to finish before printing the message

    print("Repaired file saved to:", repaired_file_path)

if __name__ == "__main__":
    main()
