# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

These tests cover the core scheduling behaviors for PawPal+, including task sorting, recurring task creation, and conflict detection when two tasks share the same time.

Example successful test run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.7, pytest-9.1.0, pluggy-6.0.0
rootdir: /Users/gabrielherrera/Documents/ai110-module2show-pawpal-starter
configfile: pytest.ini
plugins: anyio-4.2.0
collected 5 items

tests/test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.02s ===============================
```

Confidence Level: ★★★★★

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | Scheduler.sort_by_time() | Sorts tasks by clock time using a simple HH:MM conversion. |
| Filtering behavior | Scheduler.filter_tasks() | Filters tasks by pet name, completion status, or recurring status. |
| Conflict detection | Scheduler.detect_conflicts() | Returns lightweight warning messages for exact-time conflicts. |
| Recurring task logic | Scheduler.complete_task() | Marks a task complete and creates the next recurring copy for daily or weekly tasks. |

## 🎥 Demo Walkthrough

The app lets a user add a pet and save their owner name.
A user can add tasks with a time and frequency.
The scheduler sorts tasks by time and shows them in order.
The app warns about time conflicts and flags recurring tasks.
A simple workflow is add a pet → add a task → generate the schedule.

Example CLI output from running main.py:

```text
Today's Schedule
- Mochi: Morning walk at 07:30 (Pending)
- Mochi: Feed breakfast at 08:00 (Pending)
```
