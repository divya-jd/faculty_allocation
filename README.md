## CSP-FacAlloc: Faculty Subject Allocation using Constraint Satisfaction and Local Search

##  Description

**CSP-FacAlloc** is a Flask-based web application that allocates academic subjects to faculty members using **Constraint Satisfaction Problem (CSP)** techniques and **Min-Conflicts Local Search**. The system allows dynamic input of faculty preferences for each subject and ensures that assignments respect capacity and scheduling constraints.

---

##  Features

-  Web UI for selecting faculty preferences per subject
-  Allocation using Min-Conflicts local search algorithm
-  Conflict detection and count (expertise, overload, clash)
-  Subject load summary for each faculty
-  Handles timetable clashes (e.g., overlapping class hours)

---

##  Constraints Considered

1. **Faculty Expertise**: A faculty should only teach subjects they are qualified for.
2. **Max Subject Load**: A faculty can handle a maximum of **2 subjects**.
3. **Timetable Clash Avoidance**:
   - Each subject has a fixed timeslot.
   - No faculty can be assigned multiple subjects that occur at overlapping times.
4. **Minimize Conflicts**: The algorithm tries to find a valid assignment with the **least violations** of above constraints.

---

##  Tech Stack

- Python 3
- Flask (web framework)
- HTML/CSS (frontend)
- Local Search (Min-Conflicts Heuristic)

---

## Folder Structure

faculty_allocation/
├── app.py
├── templates/
│ ├── index.html
│ └── result.html

##  How to Run the App

### 1. Install Python & Flask

Make sure you have Python installed. Then install Flask:

```bash
pip install flask

### 2. Run the App

cd faculty_allocation
python app.py

### 3. Access in Browser

Visit:
http://127.0.0.1:5000