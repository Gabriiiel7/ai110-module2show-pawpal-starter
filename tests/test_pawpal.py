from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task(description="Feed fish", time="08:00")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Morning walk", time="07:30"))

    assert len(pet.tasks) == initial_count + 1


def test_sorting_correctness_returns_tasks_in_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(description="Late task", time="09:30"))
    pet.add_task(Task(description="Early task", time="07:00"))
    pet.add_task(Task(description="Mid task", time="08:15"))
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.build_daily_schedule()

    assert [task.description for _, task in sorted_tasks] == ["Early task", "Mid task", "Late task"]


def test_recurring_task_creates_next_occurrence():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    task = Task(description="Feed breakfast", time="08:00", frequency="daily")
    pet.add_task(task)
    scheduler = Scheduler(owner=owner)

    scheduler.complete_task(pet, task)

    assert task.completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[-1].frequency == "daily"
    assert pet.tasks[-1].completed is False


def test_conflict_detection_returns_warning():
    owner = Owner(name="Jordan")
    pet_one = Pet(name="Mochi", species="dog")
    pet_two = Pet(name="Luna", species="cat")
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)
    pet_one.add_task(Task(description="Morning walk", time="08:00"))
    pet_two.add_task(Task(description="Feed dinner", time="08:00"))
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Warning" in warnings[0]
