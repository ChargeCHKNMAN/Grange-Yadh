from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# [ ... student_timetables, days, time_slots ... ]  # Keep this as-is

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
        current_day_index = now.weekday()  # Monday = 0

        if current_day_index < len(days):
            today_schedule = timetable_raw[current_day_index]
            current_time = now.time()

            for idx, slot in enumerate(time_slots):
                start_time_str = slot.split(" - ")[0]
                start_time = datetime.strptime(start_time_str, "%H:%M").time()

                if current_time < start_time:
                    subject = today_schedule[idx]
                    reminder_time = (datetime.combine(now.date(), start_time) - timedelta(minutes=5)).time()
                    time_until = datetime.combine(now.date(), start_time) - now
                    mins = int(time_until.total_seconds() // 60)
                    secs = int(time_until.total_seconds() % 60)

                    next_class_info = {
                        "subject": subject,
                        "time_slot": slot,
                        "reminder_time": reminder_time.strftime("%H:%M"),
                        "time_until": f"{mins} minutes {secs} seconds"
                    }
                    break

    return render_template(
        "index.html",
        student_ids=student_ids,
        selected_student=selected_student,
        timetable=timetable,
        not_found=not_found,
        days=days,
        time_slots=time_slots,
        next_class=next_class_info
    )

if __name__ == "__main__":
    app.run(debug=True)
