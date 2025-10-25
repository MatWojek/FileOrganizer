#!/usr/bin/python3

import os
import sys
import shutil

class FileSorter: 
    def __init__(self, source_dir: str, min_size: int = 1024) -> None:
        self.source_dir = os.path.abspath(source_dir.rstrip("/"))
        self.min_size = min_size
        self.dest_dir = os.path.join(os.path.dirname(self.source_dir), "_sorted")
        os.makedirs(self.dest_dir, exist_ok=True)

    def is_empty_text_file(self, filepath: str) -> bool:
        """Check if a text/docx/pdf file is empty or nearly empty."""
        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == ".txt":
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read(200).strip()
                    return len(content) == 0
            elif ext in [".docx", ".pdf", ".doc"]:
                # simplification: consider empty if < 1 kilobyte
                return os.path.getsize(filepath) < self.min_size
        except Exception:
            return False
        return False

    def sort_files(self) -> None:
        """Sort files in the selected directory into categorized subfolders."""
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                filepath = os.path.join(root, file)

                # Skip small files
                if os.path.getsize(filepath) < self.min_size:
                    continue

                # Skip empty documents
                if self.is_empty_text_file(filepath):
                    continue

                # Get file extension
                ext = os.path.splitext(file)[1].lower().replace(".", "")
                if not ext:
                    ext = "no_extension"

                # Target folder based on extension
                target_dir = os.path.join(self.dest_dir, ext)
                os.makedirs(target_dir, exist_ok=True)

                # Move file
                try:
                    shutil.move(filepath, os.path.join(target_dir, file))
                except Exception as e:
                    print(f"Error moving {file}: {e}")