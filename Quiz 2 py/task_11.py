# Task 11 | Multi-File Student Gradebook
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def get_grade(average):
    if average >= 85:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 55:
        return "C"
    elif average >= 40:
        return "D"
    return "F"


def id_sort_key(student_id):
    # numeric IDs sort as numbers (99 before 101), other IDs sort as text
    if student_id.isdigit():
        return (0, int(student_id), student_id)
    return (1, 0, student_id)


def load_students(path):
    students = {}
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            student_id = (row.get("student_id") or "").strip()
            name = (row.get("name") or "").strip()
            if student_id == "" or name == "":
                print("Skipped student row (missing data):", row)
                continue
            if student_id in students:
                print("Skipped duplicate student ID:", student_id)
                continue
            students[student_id] = name
    return students


def load_scores(path, students):
    scores = {}      # student_id -> {subject: marks}
    rejected = []    # (row_number, reason)
    seen = set()     # (student_id, subject)

    with open(path, newline="", encoding="utf-8") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            student_id = (row.get("student_id") or "").strip()
            subject = (row.get("subject") or "").strip()

            try:
                marks = float((row.get("marks") or "").strip())
            except ValueError:
                rejected.append((row_number, "marks is not a number"))
                continue

            if student_id not in students:
                rejected.append((row_number, "unknown student ID " + student_id))
            elif subject == "":
                rejected.append((row_number, "missing subject"))
            elif not (0 <= marks <= 100):          # also rejects nan
                rejected.append((row_number, "marks must be 0-100"))
            elif (student_id, subject.casefold()) in seen:
                rejected.append((row_number, "duplicate subject for student"))
            else:
                seen.add((student_id, subject.casefold()))
                scores.setdefault(student_id, {})[subject] = marks

    return scores, rejected


def build_report(students, scores):
    with_scores = []
    without_scores = []

    for student_id, name in students.items():
        marks_list = list(scores.get(student_id, {}).values())
        if len(marks_list) == 0:
            without_scores.append(student_id)
        else:
            average = round(sum(marks_list) / len(marks_list), 2)
            with_scores.append({"student_id": student_id, "name": name,
                                "subjects": len(marks_list),
                                "average": average, "grade": get_grade(average)})

    with_scores.sort(key=lambda r: (-r["average"], id_sort_key(r["student_id"])))
    for position, row in enumerate(with_scores, start=1):
        row["rank"] = position

    for student_id in sorted(without_scores, key=id_sort_key):
        with_scores.append({"student_id": student_id, "name": students[student_id],
                            "subjects": 0, "average": "", "grade": "N/A", "rank": ""})
    return with_scores


def write_report(path, report):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["student_id", "name", "subjects",
                                                  "average", "grade", "rank"])
        writer.writeheader()
        writer.writerows(report)


if __name__ == "__main__":
    try:
        students = load_students(os.path.join(HERE, "students.csv"))
        scores, rejected = load_scores(os.path.join(HERE, "scores.csv"), students)
    except FileNotFoundError as error:
        print("Missing file:", error.filename)
    else:
        report = build_report(students, scores)
        write_report(os.path.join(HERE, "report.csv"), report)
        for row in report:
            print(row)
        print("Rejected score rows:")
        for row_number, reason in rejected:
            print("  row", row_number, "-", reason)