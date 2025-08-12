from flask import Flask, render_template, request

app = Flask(__name__)

# Timetable with 6 time slots and class numbers
student_timetables = {
    "SAY0023": [
        ["English (C3)", "English (C3)", "IT (B4)", "IT (B4)", "Business (C9)", "Business (C9)"],
        ["Business (C9)", "Physics (F4)", "Methods (C10)", "Methods (C10)", "IT (B4)", "English (C3)"],
        ["General Maths (C9)", "General Maths (C9)", "Physics (F4)", "Physics (F4)", "Methods (C10)", "Methods (C10)"],
        ["General Maths (C9)", "Methods (C10)", "IT (B4)", "IT (B4)", "English (C3)", "English (C3)"],
        ["Business (C9)", "Business (C9)", "Physics (F4)", "Physics (F4)", "General Maths (C9)", "General Maths (C9)"]
    ],
    "BINH0031": [
        ["Science (C103)", "Math (C101)", "English (C102)", "Art (C106)", "Music (C109)", "Drama (C110)"],
        ["Math (C101)", "History (C104)", "PE (C105)", "Drama (C110)", "Geography (C111)", "Music (C109)"],
        ["English (C102)", "Art (C106)", "Science (C103)", "Math (C101)", "PE (C105)", "Drama (C110)"],
        ["Math (C101)", "English (C102)", "Science (C103)", "Music (C109)", "History (C104)", "PE (C105)"],
        ["Drama (C110)", "Math (C101)", "Geography (C111)", "PE (C105)", "Art (C106)", "English (C102)"]
    ],
    "ULL0002": [
        ["Art (C106)", "Math (C101)", "Music (C109)", "Science (C103)", "Drama (C110)", "English (C102)"],
        ["English (C102)", "PE (C105)", "Math (C101)", "History (C104)", "Art (C106)", "Music (C109)"],
        ["Science (C103)", "Drama (C110)", "Math (C101)", "Music (C109)", "Geography (C111)", "PE (C105)"],
        ["Math (C101)", "Science (C103)", "English (C102)", "PE (C105)", "Art (C106)", "Drama (C110)"],
        ["History (C104)", "Math (C101)", "Science (C103)", "Music (C109)", "Drama (C110)", "English (C102)"]
    ],
    "SAD0006": [
        ["Math (C101)", "Drama (C110)", "Science (C103)", "English (C102)", "Art (C106)", "Music (C109)"],
        ["Music (C109)", "Math (C101)", "PE (C105)", "History (C104)", "Geography (C111)", "Science (C103)"],
        ["Science (C103)", "English (C102)", "Math (C101)", "Art (C106)", "PE (C105)", "Drama (C110)"],
        ["History (C104)", "Math (C101)", "Science (C103)", "Drama (C110)", "Music (C109)", "PE (C105)"],
        ["Art (C106)", "Math (C101)", "Music (C109)", "Science (C103)", "PE (C105)", "English (C102)"]
    ],
    "JAS0006": [
        ["Science (C103)", "Music (C109)", "Math (C101)", "Art (C106)", "PE (C105)", "Drama (C110)"],
        ["English (C102)", "Math (C101)", "Science (C103)", "Drama (C110)", "History (C104)", "Art (C106)"],
        ["Music (C109)", "Art (C106)", "Math (C101)", "PE (C105)", "Science (C103)", "English (C102)"],
        ["Math (C101)", "Geography (C111)", "Science (C103)", "History (C104)", "Art (C106)", "Drama (C110)"],
        ["Drama (C110)", "Math (C101)", "Science (C103)", "Music (C109)", "PE (C105)", "English (C102)"]
    ]
}

# Days and updated time slots
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "9:00 - 9:50",
    "9:50 - 10:40",
    "11:00 - 11:50",
    "11:50 - 12:40",
    "1:20 - 2:10",
    "2:10 - 3:00"
]

@app.route("/", methods=["GET", "POST"])
def index():
    student_id = ""
    timetable = None
    not_found = False

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip().upper()
        timetable = student_timetables.get(student_id)
        if timetable is None and student_id:
            not_found = True

    return render_template(
        "index.html",
        student_id=student_id,
        timetable=timetable,
        not_found=not_found,
        days=days,
        time_slots=time_slots
    )

if __name__ == "__main__":
    app.run(debug=True)

