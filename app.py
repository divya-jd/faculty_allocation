# app.py
from flask import Flask, render_template, request
import random
from collections import defaultdict

app = Flask(__name__)

faculties = ["Dr. A", "Dr. B", "Dr. C", "Dr. D"]
subjects = ["AI", "ML", "DBMS", "CN", "OS", "SE"]
max_subjects_per_faculty = 2

# Fixed timeslots for each subject (Day, Start hour, End hour)
subject_times = {
    "AI": ("Mon", 9, 10),
    "ML": ("Mon", 10, 11),
    "DBMS": ("Tue", 9, 10),
    "CN": ("Tue", 10, 11),
    "OS": ("Wed", 9, 10),
    "SE": ("Wed", 9, 10)
}

# Count conflicts (expertise, overload, time clashes)
def count_conflicts(assignment, expertise):
    conflicts = 0
    faculty_load = defaultdict(int)
    faculty_schedule = defaultdict(list)

    for subject, faculty in assignment.items():
        faculty_load[faculty] += 1
        if subject not in expertise.get(faculty, []):
            conflicts += 1
        faculty_schedule[faculty].append(subject)

    for faculty, subs in faculty_schedule.items():
        times = [subject_times[sub] for sub in subs if sub in subject_times]
        for i in range(len(times)):
            for j in range(i + 1, len(times)):
                if times[i][0] == times[j][0]:
                    if not (times[i][2] <= times[j][1] or times[j][2] <= times[i][1]):
                        conflicts += 1

    for faculty, load in faculty_load.items():
        if load > max_subjects_per_faculty:
            conflicts += (load - max_subjects_per_faculty)

    return conflicts, faculty_load

# Local search solver (min-conflicts)
def min_conflicts(expertise, max_steps=1000):
    assignment = {}
    for subject in subjects:
        possible = [f for f in faculties if subject in expertise.get(f, [])]
        assignment[subject] = random.choice(possible) if possible else random.choice(faculties)

    for _ in range(max_steps):
        conflicts, _ = count_conflicts(assignment, expertise)
        if conflicts == 0:
            return assignment

        conflict_subjects = []
        faculty_load = defaultdict(int)

        for s, f in assignment.items():
            faculty_load[f] += 1
            if s not in expertise.get(f, []) or faculty_load[f] > max_subjects_per_faculty:
                conflict_subjects.append(s)

        subject = random.choice(conflict_subjects)
        best_fac = assignment[subject]
        min_conf = float("inf")

        for fac in faculties:
            temp = assignment.copy()
            temp[subject] = fac
            conf, _ = count_conflicts(temp, expertise)
            if conf < min_conf:
                min_conf = conf
                best_fac = fac

        assignment[subject] = best_fac

    return assignment

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        expertise = {f: [] for f in faculties}
        for subject in subjects:
            selected = request.form.get(subject)
            if selected:
                expertise[selected].append(subject)

        assignment = min_conflicts(expertise)
        conflict_count, faculty_load = count_conflicts(assignment, expertise)

        return render_template(
            "result.html",
            assignment=assignment,
            conflict_count=conflict_count,
            faculty_load=faculty_load,
        )

    return render_template("index.html", subjects=subjects, faculties=faculties)

if __name__ == "__main__":
    app.run(debug=True)

