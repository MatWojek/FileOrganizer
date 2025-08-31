import os
import sys
import shutil

MIN_SIZE = 20 * 1024  # minimal size of file (20 KB)

def is_empty_text_file(filepath):
    """Check if a text/docx/pdf file is empty or nearly empty."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".txt":
            with open(filepath, "r", errors="ignore") as f:
                content = f.read(200).strip()
                return len(content) == 0
        elif ext in [".docx", ".pdf"]:
            # simplification: consider empty if <1 byte
            return os.path.getsize(filepath) < 1
    except Exception:
        return False
    return False


def sort_files(source_dir):
    # destination folder: next to the input folder
    base_dir = os.path.dirname(os.path.abspath(source_dir.rstrip("/")))
    dest_dir = os.path.join(base_dir, "_sorted")
    os.makedirs(dest_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root, file)

            # skip small files
            if os.path.getsize(filepath) < 1:
                continue

            #  skip empty documents
            if is_empty_text_file(filepath):
                continue

            # get file extension
            ext = os.path.splitext(file)[1].lower().replace(".", "")
            if not ext:
                ext = "no_extension" 

            # target folder based on extension
            target_dir = os.path.join(dest_dir, ext)
            os.makedirs(target_dir, exist_ok=True)

            # move file
            try:
                shutil.move(filepath, os.path.join(target_dir, file))
            except Exception as e:
                print(f"Error moving {file}: {e}")

    print(f"All files have been sorted into: {dest_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sort_files.py /path/to/folder")
        sys.exit(1)

    source_folder = sys.argv[1]
    if not os.path.isdir(source_folder):
        print("The provided path is not a directory!")
        sys.exit(1)

    sort_files(source_folder)
