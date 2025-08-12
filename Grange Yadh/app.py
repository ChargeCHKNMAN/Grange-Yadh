from flask import Flask, render_template, request

app = Flask(__name__)

# Student IDs
student_ids = ["SAY0023", "BINH0031", "ULL0002", "SAD0006", "JAS0006"]

# Days and time slots
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "9:00 - 9:50",
    "9:50 - 10:40",
    "11:00 - 11:50",
    "11:50 - 12:40",
    "2:10 - 3:00"
]

# Timetables: 5 students → 5 days → 5 time slots
timetables = [
    [  # SAY0023
        ["Math", "English", "Science", "History", "PE"],
        ["Biology", "Chemistry", "Math", "Art", "Music"],
        ["English", "Math", "Geography", "PE", "Drama"],
        ["History", "Science", "Math", "Music", "Art"],
        ["Math", "PE", "Science", "English", "Art"]
    ],
    [  # BINH0031
        ["Science", "Math", "English", "Art", "Music"],
        ["Math", "History", "PE", "Drama", "Geography"],
        ["English", "Art", "Science", "Math", "PE"],
        ["Math", "English", "Science", "Music", "History"],
        ["Drama", "Math", "Geography", "PE", "Art"]
    ],
    [  # ULL0002
        ["Art", "Math", "Music", "Science", "Drama"],
        ["English", "PE", "Math", "History", "Art"],
        ["Science", "Drama", "Math", "Music", "Geography"],
        ["Math", "Science", "English", "PE", "Art"],
        ["History", "Math", "Science", "Music", "Drama"]
    ],
    [  # SAD0006
        ["Math", "Drama", "Science", "English", "Art"],
        ["Music", "Math", "PE", "History", "Geography"],
        ["Science", "English", "Math", "Art", "PE"],
        ["History", "Math", "Science", "Drama", "Music"],
        ["Art", "Math", "Music", "Science", "PE"]
    ],
    [  # JAS0006
        ["Science", "Music", "Math", "Art", "PE"],
        ["English", "Math", "Science", "Drama", "History"],
        ["Music", "Art", "Math", "PE", "Science"],
        ["Math", "Geography", "Science", "History", "Art"],
        ["Drama", "Math", "Science", "Music", "PE"]
    ]
]

@app.route("/", methods=["GET", "POST"])
def index():
    timetable = None
    student_id = ""
    if request.method == "POST":
        student_id = request.form["student_id"].strip().upper()
        if student_id in student_ids:
            idx = student_ids.index(student_id)
            timetable = timetables[idx]
        else:
            timetable = "not_found"
    return render_template("index.html", student_id=student_id, timetable=timetable, days=days, time_slots=time_slots)

if __name__ == "__main__":
    app.run(debug=True)
