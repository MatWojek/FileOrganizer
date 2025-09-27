import os
import sys
import shutil


# In FUTURE this parameter is choosing in GUI
MIN_SIZE = 1024  # minimal size of file (20 KB) 

def is_empty_text_file(filepath):
    """Check if a text/docx/pdf file is empty or nearly empty."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".txt":
            with open(filepath, "r", errors="ignore") as f:
                content = f.read(200).strip()
                return len(content) == 0
        elif ext in [".docx", ".pdf", ".doc"]:
            # simplification: consider empty if < 1 kilobyte
            return os.path.getsize(filepath) < MIN_SIZE
    except Exception:
        return False
    return False


def sort_files(source_dir):
    """Sort files in the selected directory into categorized subfolders."""
    # Destination folder: next to the input folder
    base_dir = os.path.dirname(os.path.abspath(source_dir.rstrip("/")))
    dest_dir = os.path.join(base_dir, "_sorted")
    os.makedirs(dest_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root, file)

            # Skip small files
            if os.path.getsize(filepath) < MIN_SIZE:
                continue

            # Skip empty documents
            if is_empty_text_file(filepath):
                continue

            # Get file extension
            ext = os.path.splitext(file)[1].lower().replace(".", "")
            if not ext:
                ext = "no_extension"

            # Target folder based on extension
            target_dir = os.path.join(dest_dir, ext)
            os.makedirs(target_dir, exist_ok=True)

            # Move file
            try:
                shutil.move(filepath, os.path.join(target_dir, file))
            except Exception as e:
                print(f"Error moving {file}: {e}")

    print(f"All files have been sorted into: {dest_dir}")