"""
Student Academic Performance Analysis (Terminal Edition)
--------------------------------------------------------
A simple, menu-driven terminal program (pure Python, standard library only).

  1. Add Student             5. Delete Student
  2. View All Students       6. Class Performance Analysis
  3. Search Student          7. Exit
  4. Update Student Marks

UI uses pure ASCII box-drawing with emoji icons - no external rendering
dependencies beyond the standard library.
Data is stored persistently in student_data.json next to this script.

Run:  python student_performance.py
"""

import json
import os
import sys
import unicodedata

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_data.json")
WIDTH = 66  # inner width of every box

# Make sure emoji output works even when stdout is redirected/piped.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError, ValueError):
    pass


# ----------------------------------------------------------------------------
# UI helpers - ASCII box drawing (pure stdlib)
# ----------------------------------------------------------------------------
def dwidth(text):
    """Display width of a string (emoji count as 2 columns)."""
    w = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\ufe0f":  # variation selector-16 renders nothing itself
            i += 1
            continue
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            w += 2
        elif i + 1 < len(text) and text[i + 1] == "\ufe0f":
            w += 2  # base char promoted to emoji presentation
        else:
            w += 1
        i += 1
    return w


def crow(text=""):
    """Print a centered row inside the current box (width-aware)."""
    text = str(text)
    left = max(0, (WIDTH - dwidth(text)) // 2)
    right = max(0, WIDTH - dwidth(text) - left)
    print("|" + " " * left + text + " " * right + "|")


def row(text=""):
    """Print a left-aligned row inside the current box (width-aware)."""
    content = " " + str(text)
    pad = max(0, WIDTH - dwidth(content))
    print("|" + content + " " * pad + "|")


def top():
    """Double-line border - used as both the top and bottom of a box."""
    print("+" + "=" * WIDTH + "+")


def sep():
    """Single-line section divider inside a box."""
    print("+" + "-" * WIDTH + "+")


def banner(title):
    """Box header: double-line top, centered title, single-line divider."""
    top()
    crow(title)
    sep()


def msg_box(icon, msg):
    """Small standalone box for a status / error / success message."""
    print()
    top()
    row(f"{icon}  {msg}")
    top()


def warn(msg):
    """Plain inline warning (used between input prompts)."""
    print(f"    ⚠️  {msg}")


# ----------------------------------------------------------------------------
# Data handling
# ----------------------------------------------------------------------------
def load_students():
    """Load student records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("\n  Warning: could not read data file. Starting with an empty list.")
        return []


def save_students(students):
    """Save student records to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)


# ----------------------------------------------------------------------------
# Analysis helpers
# ----------------------------------------------------------------------------
def compute_result(marks):
    """Return (total, average, percentage, grade) for a list of marks."""
    total = sum(marks)
    count = len(marks) if marks else 1
    average = total / count
    percentage = average  # each subject is out of 100
    return total, average, percentage, grade_for(percentage)


def grade_for(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


def is_pass(percentage):
    return percentage >= 35


def find_student(students, roll):
    """Return the student dict with the given roll number, or None."""
    roll = roll.strip().lower()
    for s in students:
        if s["roll"].strip().lower() == roll:
            return s
    return None


# ----------------------------------------------------------------------------
# Menu options
# ----------------------------------------------------------------------------
def add_student(students):
    print()
    banner("➕  ADD NEW STUDENT")
    name = input("    Enter student name              : ").strip()
    if not name:
        msg_box("❌", "Name cannot be empty.")
        return
    roll = input("    Enter roll number               : ").strip()
    if not roll:
        msg_box("❌", "Roll number cannot be empty.")
        return
    if find_student(students, roll):
        msg_box("❌", f"A student with roll '{roll}' already exists.")
        return

    subjects = input("    Enter subject names (space-separated) : ").strip().split()
    if not subjects:
        msg_box("❌", "Enter at least one subject.")
        return

    print("    Enter marks for each subject (out of 100) :")
    marks = []
    for sub in subjects:
        while True:
            raw = input(f"       {sub} : ").strip()
            try:
                m = float(raw)
            except ValueError:
                warn("Invalid number. Try again.")
                continue
            if 0 <= m <= 100:
                marks.append(m)
                break
            warn("Marks must be between 0 and 100.")

    students.append({"name": name, "roll": roll, "subjects": subjects, "marks": marks})
    save_students(students)
    msg_box("✅", f"Student '{name}' ({roll}) added and saved.")


def view_students(students):
    print()
    banner("📋  ALL STUDENTS")
    if not students:
        row("❌  No records found. Add a student first.")
        top()
        return

    row(f"  {'Roll':<7}{'Name':<16}{'Total':<10}{'%':<9}{'Grade':<7}{'Result'}")
    row(f"  {'-' * 6:<7}{'-' * 15:<16}{'-' * 9:<10}{'-' * 7:<9}{'-' * 5:<7}{'-' * 6}")
    for s in students:
        total, _, pct, grade = compute_result(s["marks"])
        max_total = len(s["marks"]) * 100
        result = "PASS" if is_pass(pct) else "FAIL"
        row(
            f"  {s['roll'][:6]:<7}{s['name'][:15]:<16}"
            f"{f'{total:.0f}/{max_total}':<10}{pct:<9.2f}{grade:<7}{result}"
        )
    top()


def search_student(students):
    print()
    banner("🔍  SEARCH STUDENT")
    roll = input("    Enter roll number : ").strip()
    s = find_student(students, roll)
    if not s:
        msg_box("❌", f"No student found with roll '{roll}'.")
        return

    total, avg, pct, grade = compute_result(s["marks"])
    max_total = len(s["marks"]) * 100
    result = "PASS" if is_pass(pct) else "FAIL"
    res_icon = "✅" if is_pass(pct) else "❌"

    print()
    top()
    crow(f"📝  REPORT : {s['name']}   ({s['roll']})")
    sep()
    row(f"  {'Subject':<24}Marks (out of 100)")
    row(f"  {'-' * 22:<24}{'-' * 18}")
    for sub, m in zip(s["subjects"], s["marks"]):
        row(f"  {sub[:22]:<24}{m:.1f}")
    sep()
    row(f"📊  Total      : {total:.1f} / {max_total}")
    row(f"📐  Average    : {avg:.2f}")
    row(f"📈  Percentage : {pct:.2f}%")
    row(f"🏅  Grade      : {grade}")
    row(f"{res_icon}  Result     : {result}")
    top()


def update_student(students):
    print()
    banner("✏️   UPDATE STUDENT MARKS")
    roll = input("    Enter roll number : ").strip()
    s = find_student(students, roll)
    if not s:
        msg_box("❌", f"No student found with roll '{roll}'.")
        return

    print(f"\n    Student : {s['name']} ({s['roll']})")
    print(f"    Subjects: {', '.join(s['subjects'])}")
    print("    Enter new marks for each subject (out of 100) :")
    new_marks = []
    for sub, old in zip(s["subjects"], s["marks"]):
        while True:
            raw = input(f"       {sub} (current {old:.1f}) : ").strip()
            try:
                m = float(raw)
            except ValueError:
                warn("Invalid number. Try again.")
                continue
            if 0 <= m <= 100:
                new_marks.append(m)
                break
            warn("Marks must be between 0 and 100.")

    s["marks"] = new_marks
    save_students(students)
    msg_box("✅", f"Marks updated for '{s['name']}' ({s['roll']}).")


def delete_student(students):
    print()
    banner("🗑️   DELETE STUDENT")
    roll = input("    Enter roll number : ").strip()
    s = find_student(students, roll)
    if not s:
        msg_box("❌", f"No student found with roll '{roll}'.")
        return

    confirm = input(f"    Delete '{s['name']}' ({s['roll']})? (y/n) : ").strip().lower()
    if confirm != "y":
        msg_box("⚠️", "Deletion cancelled. Nothing was removed.")
        return

    students.remove(s)
    save_students(students)
    msg_box("✅", f"Student '{s['name']}' ({s['roll']}) deleted.")


def class_analysis(students):
    print()
    banner("📊  CLASS PERFORMANCE ANALYSIS")
    if not students:
        row("❌  No records found. Add a student first.")
        top()
        return

    results = []
    for s in students:
        total, avg, pct, grade = compute_result(s["marks"])
        results.append((s, total, pct, grade))

    class_avg = sum(r[2] for r in results) / len(results)
    topper = max(results, key=lambda r: r[2])
    lowest = min(results, key=lambda r: r[2])
    passed = sum(1 for r in results if is_pass(r[2]))
    failed = len(results) - passed

    row(f"👥  Total students : {len(results)}")
    row(f"📐  Class average  : {class_avg:.2f}%")
    row(f"🏆  Highest scorer : {topper[0]['name'][:14]} ({topper[0]['roll']}) - {topper[2]:.2f}% ({topper[3]})")
    row(f"📉  Lowest scorer  : {lowest[0]['name'][:14]} ({lowest[0]['roll']}) - {lowest[2]:.2f}% ({lowest[3]})")
    row(f"✅  Passed         : {passed}")
    row(f"❌  Failed         : {failed}")
    sep()
    crow("🏅  GRADE DISTRIBUTION")
    dist = {}
    for _, _, _, grade in results:
        dist[grade] = dist.get(grade, 0) + 1
    for g in ["A+", "A", "B", "C", "D", "F"]:
        if g in dist:
            row(f"      {g}  :  {dist[g]}")
    top()


# ----------------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------------
def show_menu():
    print()
    top()
    crow("")
    crow("🎓  STUDENT ACADEMIC PERFORMANCE ANALYSIS  📊")
    crow("")
    sep()
    row("  1.  ➕   Add Student")
    row("  2.  📋   View All Students")
    row("  3.  🔍   Search Student (Detailed Report)")
    row("  4.  ✏️   Update Student Marks")
    row("  5.  🗑️   Delete Student")
    row("  6.  📊   Class Performance Analysis")
    row("  7.  🚪   Exit")
    top()


def main():
    students = load_students()
    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": class_analysis,
    }

    while True:
        show_menu()
        choice = input("\n  Enter your choice (1-7) : ").strip()

        if choice == "7":
            save_students(students)
            print("\n  Data saved. Goodbye!\n")
            break

        action = actions.get(choice)
        if action is None:
            print("  Invalid choice. Please enter a number from 1 to 7.")
            continue

        try:
            action(students)
        except KeyboardInterrupt:
            print("\n\n  Operation cancelled by user.")
        except EOFError:
            print("\n\n  Input stream closed. Exiting.")
            save_students(students)
            break


if __name__ == "__main__":
    main()




