from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# --- Timetable Data ---
student_timetables = {
    "SAY0023": [
        ["English (C3)", "English (C3)", "IT (B4)", "IT (B4)", "Business (C9)", "Business (C9)"],
        ["Business (C9)", "Physics (F4)", "Methods (C10)", "Methods (C10)", "IT (B4)", "English (C3)"],
        ["General Maths (C9)", "General Maths (C9)", "Physics (F4)", "Physics (F4)", "Methods (C10)", "Methods (C10)"],
        ["General Maths (C9)", "Methods (C10)", "IT (B4)", "IT (B4)", "English (C3)", "English (C3)"],
        ["Business (C9)", "Business (C9)", "Physics (F4)", "Physics (F4)", "General Maths (C9)", "General Maths (C9)"]
    ],
    "SAD0006": [
        ["English (C4)", "English (C4)", "IT (B4)", "IT (B4)", "History (C3)", "History (C3)"],
        ["History (C3)", "Math (C10)", "Psychology (D8)", "Psychology (D8)", "IT (B4)", "English (C4)"],
        ["Business (C2)", "Business (C2)", "Math (C10)", "Math (C10)", "Psychology (D8)", "Psychology (D8)"],
        ["Business (C2)", "Psychology (E2)", "IT (B4)", "IT (B4)", "English (C4)", "English (C4)"],
        ["History (C3)", "History (C3)", "Math (C10)", "Math (C10)", "Business (C2)", "Business (C2)"]
    ],
    # Add more students if needed...
}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

time_slots = [
    "9:00 - 9:50",
    "9:50 - 10:40",
    "11:00 - 11:50",
    "11:50 - 12:40",
    "1:20 - 2:10",
    "2:10 - 3:00"
]

@app.route("/", methods=["GET"])
def index():
    student_ids = list(student_timetables.keys())
    selected_student = request.args.get("student_id", "")
    timetable_raw = student_timetables.get(selected_student)
    not_found = timetable_raw is None
    timetable = list(zip(days, timetable_raw)) if timetable_raw else []

    next_class_info = None

    if timetable_raw:
        now = datetime.now()
        current_day_index = now.weekday()  # Monday = 0, Sunday = 6

        if current_day_index < len(days):
            today_schedule = timetable_raw[current_day_index]
            current_time = now.time()

            for idx, slot in enumerate(time_slots):
                start_str, end_str = slot.split(" - ")
                start_time = datetime.strptime(start_str, "%H:%M").time()
                end_time = datetime.strptime(end_str, "%H:%M").time()

                if current_time < start_time:
                    subject = today_schedule[idx]
                    class_start_dt = datetime.combine(now.date(), start_time)
                    reminder_dt = class_start_dt - timedelta(minutes=5)
                    time_until = class_start_dt - now

                    mins = int(time_until.total_seconds() // 60)
                    secs = int(time_until.total_seconds() % 60)

                    next_class_info = {
                        "subject": subject,
                        "time_slot": slot,
                        "reminder_time": reminder_dt.strftime("%H:%M"),
                        "time_until": f"{mins} minutes {secs} seconds"
                    }
                    break

    return render_template(
        "index.html",
        student_ids=student_ids,
        selected_student=selected_student,
        timetable=timetable,
        not_found=not_found,
        time_slots=time_slots,
        next_class=next_class_info
    )

if __name__ == "__main__":
    app.run(debug=True)
