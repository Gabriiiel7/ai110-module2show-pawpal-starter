from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Jordan")
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")
owner.add_pet(mochi)
owner.add_pet(luna)

morning_walk = Task(description="Morning walk", time="07:30")
dinner = Task(description="Dinner", time="19:00", frequency="daily")
feed_breakfast = Task(description="Feed breakfast", time="08:00")
play_time = Task(description="Play time", time="09:00")
conflict_task = Task(description="Vet check", time="07:30", frequency="weekly")

mochi.add_task(morning_walk)
mochi.add_task(dinner)
mochi.add_task(conflict_task)
mochi.add_task(feed_breakfast)
luna.add_task(play_time)

scheduler = Scheduler(owner=owner)
scheduler.complete_task(mochi, dinner)

print("Sorted schedule:")
for pet, task in scheduler.sort_by_time():
    status = "Done" if task.completed else "Pending"
    print(f"- {pet.name}: {task.description} at {task.time} ({status})")

print("\nPending tasks for Mochi:")
for pet, task in scheduler.filter_tasks(pet_name="Mochi", completed=False):
    print(f"- {pet.name}: {task.description} at {task.time}")

print("\nRecurring tasks:")
for pet, task in scheduler.get_recurring_tasks():
    print(f"- {pet.name}: {task.description} ({task.frequency})")

print("\nConflict warnings:")
for warning in scheduler.detect_conflicts():
    print(f"- {warning}")
