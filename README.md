# FileOrganizer

---

File Organizer is a Python utility that helps organize large collections of files. 
It automatically moves files into subfolders based on their extensions, skips small 
or empty documents, and supports batch processing of multiple directories. 
Ideal for cleaning up downloads, recovered files, or messy folders efficiently.

--- 

## Goal

--- 

In the future this will be AI-based photo organization tool designed to automatically 
categorize and sort images into meaningful folders. Instead of spending hours manually moving 
files, you provide the application with a reference dataset of already sorted photos. 
Using this dataset, the AI learns to recognize categories (such as family, pets, holidays, landscapes) 
and then applies this knowledge to classify and sort new, unsorted images.

This project aims to make photo management faster, smarter, and more intuitive. 
It can be adapted for personal use (organizing family albums), professional workflows 
(photographers sorting thousands of shots), or specialized domains (medical imaging, research datasets, etc.).

--- 

## Features

---

- Sorts files into folders by extension
- Skips small files (less than 20 KB by default)
- Skips empty or nearly empty documents (`.txt`, `.docx`, `.pdf`)
- Creates a single `_sorted` folder next to the source folder
- Works on multiple types of files and nested directories

---

## Requirements

---

- Python 3.x
- Works on Linux, macOS, and Windows (with Python installed)

---

## Usage

---

1. Clone the repository:

```bash
git clone https://github.com/MatWojas/FileOrganizer.git
cd FileOrganizer
```
2. Run the script:

- If you want to sort only one folder:

```
python3 sort_files.py /path/to/your/folder 
```

- Else change the `dir` in loop.sh and number of iteration and then:

```
chmod +x loops.sh
./loops.sh
```

--- 

## Results

---

- The script will create a _sorted folder next to the provided folder.
- Files will be moved into subfolders based on their extensions.
- Small or empty files will be skipped.
- Extra: if you use loops.sh the empty dictionary will be removed

---

## Example

---

- Before:

```
my_folder/
├── file1.txt
├── file2.pdf
├── image.jpg
└── document.docx
```
- After:

```
my_folder/
└── _sorted/
    ├── txt/
    │   └── file1.txt
    ├── pdf/
    │   └── file2.pdf
    ├── jpg/
    │   └── image.jpg
    └── docx/
        └── document.docx
```

--- 

## Notes

---

- The script moves files, it does not copy them. Be careful if you need backups.

- Files without an extension are placed in the no_extension/ folder.

- You can modify MIN_SIZE in the script to change the minimum size threshold.

--- 

## Roadmap 

---

- Add GUI for easy drag-and-drop sorting
- Support for cloud storage (Google Drive, OneDrive, etc.)
- Improve accuracy with transfer learning models (ResNet, EfficientNet)
- Add duplicate photo detection
- Adding sorting based on date, name and else

--- 

## License

---

This project is licensed under the MIT License.

--- 

## Author

Created by an enthusiastic programmer with a passion for AI-powered content. The author is MatWojas.

---
