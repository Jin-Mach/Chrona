# Chrona

A file transfer and organization tool for moving or copying files and folders into a structured target directory based on user-defined rules.

Chrona allows flexible filtering, automatic sorting, and configurable naming rules, all with a simple UI and persistent settings.

---

## Features

### File transfer
- Drag & drop support for files and folders
- Manual file/folder selection via dialog
- Target directory selection
- Displays selected item statistics (files, folders, total items)
- Review and remove items from selection list
- Clear selection list
- Start transfer with current settings

---

### Folder structure rules
- Organize files by date:
  - Year
  - Month (depends on year)
  - Day (depends on month)
- Organize by file type
- Option to include hidden files

---

### File filtering
- Enable/disable main filtering system
- Predefined categories:
  - documents
  - text files
  - Office files
  - images
  - music
  - archives
- Custom file extensions support (e.g. .pdf)

---

### File naming rules
- Default or custom filename
- Custom naming supports:
  - timestamp
  - counter
- At least one dynamic element must be enabled when using custom naming

---

### Conflict handling
- Auto-rename duplicates (e.g. file(1).txt)
- Option to show skipped files

---

### Transfer behavior
- Choose action for source files:
  - keep original
  - move to trash
  - delete permanently
- Option to show files that were not processed

---

### Progress & control
- Progress indicator (e.g. 3/10 files processed)
- Cancel operation at any time
- Pause supported between file operations
- Final summary after completion
- List of failed files available after transfer

---

### Settings
- Default source and destination paths
- Settings are automatically saved on exit (except custom naming state)
- Persistent configuration loaded on startup

---

## Installation

(Tested on Windows / macOS, development environment: PyCharm)

- Navigate to the project directory:
```bash
    cd Chrona
```

- Create a virtual environment:
  - On Windows
  ```bash
  python -m venv .venv
  ```
  - On macOS/Linux
  ```bash
  python3 -m venv .venv
  ```

- Activate the virtual environment:
  - On Windows (Command Prompt): 
  ```bash
  .venv\Scripts\activate
  ```
  - On Windows (PowerShell):
  ```bash
  .venv\Scripts\activate.ps1
  ```
  - On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

- Install the required packages:
  - On Windows
  ```bash
  python -m pip install -r requirements.txt
  ```
  - On macOS/Linux
  ```bash
  python3 -m pip install -r requirements.txt
  ```

## Usage
After installing the dependencies, you can start the application with the following command:

- Run the application:
  - On Windows
  ```bash
  python chrona.py
  ```
  - On macOS/Linux
  ```bash
  python3 chrona.py
  ```

## License

- This project is licensed under the MIT License.


## Contact
- If you have any questions or feedback, feel free to reach out via my GitHub profile: [Jin-Mach](https://github.com/Jin-Mach).