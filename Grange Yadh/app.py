from flask import Flask, render_template, request

app = Flask(__name__)

# Student timetables as a dictionary for easier lookup
student_timetables = {
    "SAY0023": [
        ["Math", "English", "Science", "History", "PE"],
        ["Biology", "Chemistry", "Math", "Art", "Music"],
        ["English", "Math", "Geography", "PE", "Drama"],
        ["History", "Science", "Math", "Music", "Art"],
        ["Math", "PE", "Science", "English", "Art"]
    ],
    "BINH0031": [
        ["Science", "Math", "English", "Art", "Music"],
        ["Math", "History", "PE", "Drama", "Geography"],
        ["English", "Art", "Science", "Math", "PE"],
        ["Math", "English", "Science", "Music", "History"],
        ["Drama", "Math", "Geography", "PE", "Art"]
    ],
    "ULL0002": [
        ["Art", "Math", "Music", "Science", "Drama"],
        ["English", "PE", "Math", "History", "Art"],
        ["Science", "Drama", "Math", "Music", "Geography"],
        ["Math", "Science", "English", "PE", "Art"],
        ["History", "Math", "Science", "Music", "Drama"]
    ],
    "SAD0006": [
        ["Math", "Drama", "Science", "English", "Art"],
        ["Music", "Math", "PE", "History", "Geography"],
        ["Science", "English", "Math", "Art", "PE"],
        ["History", "Math", "Science", "Drama", "Music"],
        ["Art", "Math", "Music", "Science", "PE"]
    ],
    "JAS0006": [
        ["Science", "Music", "Math", "Art", "PE"],
        ["English", "Math", "Science", "Drama", "History"],
        ["Music", "Art", "Math", "PE", "Science"],
        ["Math", "Geography", "Science", "History", "Art"],
        ["Drama", "Math", "Science", "Music", "PE"]
    ]
}

# Days and time slots
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "9:00 - 9:50",
    "9:50 - 10:40",
    "11:00 - 11:50",
    "11:50 - 12:40",
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
