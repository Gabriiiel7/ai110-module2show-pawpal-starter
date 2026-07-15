import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ app.

This version uses the backend logic layer to keep pets and tasks in memory while you use the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner track care tasks for their pets.
"""
    )

st.divider()

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Save owner name"):
    owner.name = owner_name
    st.success("Owner name updated.")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted = st.form_submit_button("Add pet")

    if submitted:
        if pet_name.strip():
            new_pet = Pet(name=pet_name.strip(), species=species)
            owner.add_pet(new_pet)
            st.success(f"{new_pet.name} was added.")
        else:
            st.warning("Please enter a pet name.")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    selected_pet_name = st.selectbox("Select pet", [pet.name for pet in owner.pets])
    selected_pet = owner.get_pet(selected_pet_name)

    task_description = st.text_input("Task description", value="Morning walk")
    task_time = st.text_input("Time", value="07:30")
    task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        if selected_pet:
            task = Task(description=task_description, time=task_time, frequency=task_frequency)
            selected_pet.add_task(task)
            st.success(f"Task added for {selected_pet.name}.")
        else:
            st.warning("Please select a pet.")

    if selected_pet and selected_pet.tasks:
        st.write("Current tasks:")
        for task in selected_pet.tasks:
            status = "Done" if task.completed else "Pending"
            st.write(f"- {task.description} at {task.time} ({status})")
    elif selected_pet:
        st.info("No tasks yet for this pet.")
else:
    st.info("Add a pet first to create tasks.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    sorted_schedule = scheduler.build_daily_schedule()
    pending_tasks = scheduler.filter_tasks(items=sorted_schedule, completed=False)
    recurring_tasks = scheduler.get_recurring_tasks(items=pending_tasks)
    conflict_warnings = scheduler.detect_conflicts(items=sorted_schedule)

    if pending_tasks:
        st.success("Your schedule is ready and sorted by time.")
        rows = [
            {
                "Pet": pet.name,
                "Task": task.description,
                "Time": task.time,
                "Frequency": task.frequency,
                "Status": "Pending",
            }
            for pet, task in pending_tasks
        ]
        st.table(rows)
    else:
        st.info("No pending tasks to show right now.")

    if recurring_tasks:
        st.caption("Recurring tasks:")
        for pet, task in recurring_tasks:
            st.write(f"- {pet.name}: {task.description} at {task.time} ({task.frequency})")

    if conflict_warnings:
        st.warning("Potential conflicts found:")
        for warning in conflict_warnings:
            st.warning(warning)

    if pending_tasks:
        st.subheader("Quick actions")
        for pet, task in pending_tasks:
            if st.button(
                f"Mark complete: {pet.name} - {task.description}",
                key=f"complete_{pet.name}_{task.description}_{task.time}",
            ):
                scheduler.complete_task(pet, task)
                st.success(f"Marked '{task.description}' complete.")
                st.rerun()
