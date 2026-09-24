# Student Academic Performance Analysis

A menu-driven terminal application built with pure Python for managing and analysing student academic records. Instead of maintaining marks in physical registers, the program lets you enter subject-wise marks once and then automatically handles every calculation — total, average, percentage, grade and pass/fail — along with a class-wide analysis covering the topper, lowest scorer and grade distribution. All records are stored permanently in a JSON file, so nothing is lost between sessions. The interface is a clean boxed menu with emoji icons, and the app runs entirely on the Python standard library with nothing to install.

## Features

- **Complete record management** — add, view, search, update and delete student records through a numbered menu.
- **Automatic results** — total marks, average, percentage, grade and PASS/FAIL are calculated for every student.
- **Class analysis** — one option shows the class average, highest and lowest scorer, pass/fail counts and grade distribution.
- **Persistent storage** — records are written to a JSON file after every change and loaded automatically at startup.
- **Input validation** — marks must be between 0 and 100, roll numbers must be unique, and empty fields are rejected.
- **Lightweight** — uses only the Python standard library (`json`, `os`, `sys`, `unicodedata`); no third-party packages.
- **Clean terminal UI** — output is presented in ASCII boxes so tables and reports are easy to read.

## Menu Options

| # | Option | Description |
| - | ------ | ----------- |
| 1 | Add Student | Register a new student with name, roll number, subjects and marks |
| 2 | View All Students | Table of every student with total, percentage, grade and result |
| 3 | Search Student | Detailed subject-wise report for a single roll number |
| 4 | Update Student Marks | Replace the marks of an existing student |
| 5 | Delete Student | Remove a record after y/n confirmation |
| 6 | Class Performance Analysis | Class statistics and grade distribution |
| 7 | Exit | Saves data and closes the program |

## Grading System

Marks are entered out of 100 for each subject. The percentage is the average of all subjects.

| Grade | Percentage | Result |
| ----- | ---------- | ------ |
| A+ | 90 - 100 | PASS |
| A | 80 - 89.99 | PASS |
| B | 70 - 79.99 | PASS |
| C | 60 - 69.99 | PASS |
| D | 50 - 59.99 | PASS |
| F | Below 50 | FAIL |

A student is considered passed when the percentage is **35% or above**.

## Data Storage

Records are stored as a JSON array in:

```
D:\Student Records\Student Data\student_data.json
```

- The folder is created automatically on first run.
- The file is re-written after every add, update or delete.
- To store data somewhere else, change the `DATA_DIR` variable at the top of `student_performance.py`.

Each record has the following structure:

```json
{
    "name": "Alice",
    "roll": "S001",
    "subjects": ["Math", "Science", "English"],
    "marks": [85.0, 90.0, 88.0]
}
```

## How It Works

The program is organised into small, focused functions:

| Function | Responsibility |
| -------- | -------------- |
| `load_students()` / `save_students()` | Read and write the JSON data file |
| `add_student()` / `view_students()` / `search_student()` | Record management and reporting |
| `update_student()` / `delete_student()` | Modify or remove existing records |
| `compute_result()` / `grade_for()` / `is_pass()` | Calculate totals, percentage, grade and result |
| `class_analysis()` | Class average, topper, lowest scorer, pass/fail, grade distribution |
| `banner()` / `row()` / `crow()` / `msg_box()` | Draw the boxed terminal interface |

On startup the saved records are loaded into a list; every operation updates that list and immediately saves it back to disk, so the file always reflects the latest data.

## Sample Output

```
+==================================================================+
|                                                                  |
|          🎓  STUDENT ACADEMIC PERFORMANCE ANALYSIS  📊           |
|                                                                  |
+------------------------------------------------------------------+
|   1.  ➕   Add Student                                           |
|   2.  📋   View All Students                                     |
|   3.  🔍   Search Student (Detailed Report)                      |
|   4.  ✏️   Update Student Marks                                  |
|   5.  🗑️   Delete Student                                        |
|   6.  📊   Class Performance Analysis                            |
|   7.  🚪   Exit                                                  |
+==================================================================+

  Enter your choice (1-7) :
```

## Requirements

- Python 3.10 or later
- Windows, Linux or macOS with any standard terminal
- No third-party packages and no internet connection

## Running the Program

```bash
python student_performance.py
```

Then choose an option from the menu and follow the prompts. Marks are entered one per line, and data saves automatically after each change.

## Project Structure

```
student-academic-performance-analysis/
├── student_performance.py   # main program (pure Python)
├── student_data.json        # student records (auto-created)
└── README.md
```
