from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

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
        ["English (C4)", "English (C4)", "IT (B4)", "IT (B4)", "History (C3)", "History (C3)"],
        ["History (C3)", "Math (C10)", "Psychology (D8)", "Psychology (D8)", "IT (B4)", "English (C4)"],
        ["Business (C2)", "Business (C2)", "Math (C10)", "Math (C10)", "Psychology (D8)", "Psychology (D8)"],
        ["Business (C2)", "Psychology (E2)", "IT (B4)", "IT (B4)", "English (C4)", "English (C4)"],
        ["History (C3)", "History (C3)", "Math (C10)", "Math (C10)", "Business (C2)", "Business (C2)"]
    ],
    "JAS0006": [
        ["Science (C103)", "Music (C109)", "Math (C101)", "Art (C106)", "PE (C105)", "Drama (C110)"],
        ["English (C102)", "Math (C101)", "Science (C103)", "Drama (C110)", "History (C104)", "Art (C106)"],
        ["Music (C109)", "Art (C106)", "Math (C101)", "PE (C105)", "Science (C103)", "English (C102)"],
        ["Math (C101)", "Geography (C111)", "Science (C103)", "History (C104)", "Art (C106)", "Drama (C110)"],
        ["Drama (C110)", "Math (C101)", "Science (C103)", "Music (C109)", "PE (C105)", "English (C102)"]
    ]
}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Use datetime objects for time slots (start, end)
time_slots = [
    (datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("09:50", "%H:%M").time()),
    (datetime.strptime("09:50", "%H:%M").time(), datetime.strptime("10:40", "%H:%M").time()),
    (datetime.strptime("11:00", "%H:%M").time(), datetime.strptime("11:50", "%H:%M").time()),
    (datetime.strptime("11:50", "%H:%M").time(), datetime.strptime("12:40", "%H:%M").time()),
    (datetime.strptime("13:20", "%H:%M").time(), datetime.strptime("14:10", "%H:%M").time()),
    (datetime.strptime("14:10", "%H:%M").time(), datetime.strptime("15:00", "%H:%M").time())
]

def format_time_slot(slot):
    start_str = slot[0].strftime("%-H:%M") if hasattr(slot[0], 'strftime') else slot[0].strftime("%H:%M")
    end_str = slot[1].strftime("%-H:%M") if hasattr(slot[1], 'strftime') else slot[1].strftime("%H:%M")
    return f"{start_str} - {end_str}"

def get_next_class(timetable, time_slots):
    now = datetime.now()
    today_idx = now.weekday()
    if today_idx > 4:
        # Weekend - treat as Monday next week
        days_until_monday = 7 - today_idx
        now = now + timedelta(days=days_until_monday)
        today_idx = 0

    for day_offset in range(5):
        day_idx = (today_idx + day_offset) % 5
        classes_today = timetable[day_idx]

        class_date = (now + timedelta(days=day_offset)).date()

        for i, slot in enumerate(time_slots):
            start_time, end_time = slot
            class_start = datetime.combine(class_date, start_time)
            class_end = datetime.combine(class_date, end_time)

            if class_start > now:
                time_until = class_start - now
                minutes, seconds = divmod(time_until.seconds, 60)
                reminder_dt = class_start - timedelta(minutes=5)
                reminder_time = reminder_dt.strftime("%H:%M")
                slot_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                return {
                    "subject": classes_today[i],
                    "time_slot": slot_str,
                    "time_until": f"{minutes} minutes {seconds} seconds",
                    "reminder_time": reminder_time,
                    "class_start_iso": class_start.isoformat()
                }
    return None

@app.route("/", methods=["GET"])
def index():
    student_ids = list(student_timetables.keys())
    selected_student = request.args.get("student_id", student_ids[0])
    timetable_raw = student_timetables.get(selected_student)
    not_found = timetable_raw is None
    timetable = list(zip(days, timetable_raw)) if timetable_raw else []

    next_class = None
    if timetable_raw:
        next_class = get_next_class(timetable_raw, time_slots)

    # Format timetable for display (convert times to strings)
    formatted_time_slots = [f"{slot[0].strftime('%H:%M')} - {slot[1].strftime('%H:%M')}" for slot in time_slots]

    return render_template(
        "index.html",
        student_ids=student_ids,
        selected_student=selected_student,
        timetable=timetable,
        not_found=not_found,
        days=days,
        time_slots=formatted_time_slots,
        next_class=next_class
    )

if __name__ == "__main__":
    app.run(debug=True)
