from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample timetable data for demonstration
# Format: { student_id: { day: [subject per slot] } }
TIMETABLES = {
    "SAY0023": {
        "Monday":    ["Math", "Physics", "Chemistry", "English", "PE"],
        "Tuesday":   ["Biology", "Math", "History", "Geography", "Art"],
        "Wednesday": ["Physics", "Chemistry", "Math", "English", "Music"],
        "Thursday":  ["Math", "Biology", "PE", "History", "Physics"],
        "Friday":    ["English", "Math", "Chemistry", "Geography", "Computer Science"],
    },
    "SAY0101": {
        "Monday":    ["English", "Math", "Physics", "History", "PE"],
        "Tuesday":   ["Math", "Chemistry", "Biology", "Art", "Music"],
        "Wednesday": ["Geography", "English", "Math", "Physics", "Computer Science"],
        "Thursday":  ["History", "Math", "Chemistry", "PE", "Biology"],
        "Friday":    ["Physics", "English", "Math", "Art", "Music"],
    }
}

# Time slots for classes (5 slots, example)
TIME_SLOTS = [
    "08:30 - 09:20",
    "09:25 - 10:15",
    "10:20 - 11:10",
    "11:15 - 12:05",
    "12:10 - 13:00"
]

# Convert time slot string to datetime.time for comparison
def parse_slot_start_time(slot_str):
    # e.g. "08:30 - 09:20" -> datetime.time(8,30)
    start_str = slot_str.split('-')[0].strip()
    return datetime.strptime(start_str, "%H:%M").time()

@app.route("/", methods=["GET"])
def index():
    student_id = request.args.get("student_id", "").strip().upper()
    not_found = False
    timetable_data = []
    next_class_info = None

    if student_id:
        if student_id not in TIMETABLES:
            not_found = True
        else:
            student_timetable = TIMETABLES[student_id]
            # Prepare timetable as list of (day, [subjects]) for template
            timetable_data = [(day, student_timetable.get(day, [""]*len(TIME_SLOTS))) for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]

            # Find next class based on current datetime
            now = datetime.now()

            # We assume classes happen Mon-Fri only
            # Find today or next day with a class coming
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            today_weekday = now.weekday()  # Monday=0 ... Friday=4
            found_next = False

            for day_offset in range(5):
                check_day_index = (today_weekday + day_offset) % 5
                day_name = days_of_week[check_day_index]

                classes = student_timetable.get(day_name, [])
                if not classes:
                    continue

                # Calculate date for that day
                day_date = now.date() + timedelta(days=day_offset)

                for idx, subject in enumerate(classes):
                    if subject.strip() == "":
                        continue
                    slot_start_time = parse_slot_start_time(TIME_SLOTS[idx])
                    slot_start_dt = datetime.combine(day_date, slot_start_time)

                    if slot_start_dt > now:
                        # Next class found
                        time_until = slot_start_dt - now
                        minutes, seconds = divmod(time_until.seconds, 60)
                        time_until_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                        reminder_dt = slot_start_dt - timedelta(minutes=5)
                        reminder_time_str = reminder_dt.strftime("%Y-%m-%d %H:%M:%S")
                        next_class_info = {
                            "subject": subject,
                            "time_slot": TIME_SLOTS[idx],
                            "start_datetime": slot_start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            "time_until": time_until_str,
                            "reminder_time": reminder_time_str
                        }
                        found_next = True
                        break
                if found_next:
                    break

    return render_template(
        "index.html",
        selected_student=student_id,
        timetable=timetable_data,
        time_slots=TIME_SLOTS,
        not_found=not_found,
        next_class=next_class_info,
    )


if __name__ == "__main__":
    app.run(debug=True)
