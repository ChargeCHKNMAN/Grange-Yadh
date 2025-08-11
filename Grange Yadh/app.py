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
        ["Science"]()
