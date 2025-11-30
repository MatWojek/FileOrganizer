# FileOrganizer

File Organizer is a Python utility that helps organize large collections
of files. It automatically moves files into subfolders based on their
extensions, skips small or empty documents, and supports batch
processing of multiple directories. Ideal for cleaning up downloads,
recovered files, or messy folders efficiently.

## Features

-   Sorts files into folders by extension\
-   Skips small files (less than 20 KB by default)\
-   Skips empty or nearly empty documents (`.txt`, `.docx`, `.pdf`)\
-   Creates a single `_sorted` folder next to the source folder\
-   Works on multiple types of files and nested directories

## Requirements

-   Python 3.x\
-   Works on Linux, macOS, and Windows (with Python installed)

## Usage

1.  **Clone the repository:**

``` bash
git clone https://github.com/MatWojas/FileOrganizer.git
cd FileOrganizer
```

2.  **Create and activate a virtual environment (optional but
    recommended):**

**Linux/macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

3.  **Install required Python packages:**

All required modules are listed in `requirements.txt`:

``` bash
pip install -r requirements.txt
```

4.  **Run the program (without VS Code):**

Linux/macOS:

``` bash
python3 app.py
```

Windows:

``` bash
python app.py
```

After running the program, the application window will appear --- click
**Sort Files**, select a folder and you're done.

## Results

-   The script will create a `_sorted` folder next to the provided
    folder.\
-   Files will be moved into subfolders based on their extensions.\
-   Small or empty files will be skipped.\
-   Extra: if you use `loops.sh`, empty directories will be removed.

## Example

**Before:**

    my_folder/
    ├── file1.txt
    ├── file2.pdf
    ├── image.jpg
    └── document.docx

**After:**

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

## Notes

-   The script *moves* files --- it does not copy them.\
-   Files without an extension are placed in the `no_extension/`
    folder.\
-   You can modify `MIN_SIZE` in the script to change the minimum size
    threshold.

## License

This project is licensed under the MIT License.

## Author

Created by an enthusiastic programmer with a passion for AI-powered
content.\
Author: **MatWojek**
