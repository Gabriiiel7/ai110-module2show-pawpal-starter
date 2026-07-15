from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as still pending."""
        self.completed = False

    def edit(self, description: str | None = None, time: str | None = None,
             frequency: str | None = None) -> None:
        """Update the task details when new values are provided."""
        if description is not None:
            self.description = description
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency


@dataclass
class Pet:
    name: str
    species: str
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are still unfinished."""
        return [task for task in self.tasks if not task.completed]

    def update_info(self, name: str | None = None, species: str | None = None,
                    notes: str | None = None) -> None:
        """Update the pet's basic information."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if notes is not None:
            self.notes = notes


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Collect every task from all pets for the owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    owner: Owner

    def _time_to_minutes(self, time_value: str) -> int:
        """Convert a HH:MM string into minutes for sorting."""
        try:
            hours, minutes = time_value.split(":")
            return int(hours) * 60 + int(minutes)
        except ValueError:
            return 24 * 60

    def sort_by_time(self, items: List[tuple[Pet, Task]] | None = None) -> List[tuple[Pet, Task]]:
        """Sort tasks by their clock time."""
        schedule = items if items is not None else self.build_daily_schedule()
        return sorted(schedule, key=lambda item: self._time_to_minutes(item[1].time))

    def build_daily_schedule(self) -> List[tuple[Pet, Task]]:
        """Create a sorted list of tasks for the day."""
        all_items: List[tuple[Pet, Task]] = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_items.append((pet, task))
        return self.sort_by_time(all_items)

    def filter_tasks(self, items: List[tuple[Pet, Task]] | None = None, pet_name: str | None = None,
                     completed: bool | None = None, recurring: bool | None = None) -> List[tuple[Pet, Task]]:
        """Filter tasks by pet, completion state, or recurring status."""
        schedule = items if items is not None else self.build_daily_schedule()
        filtered: List[tuple[Pet, Task]] = []
        for pet, task in schedule:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            if completed is not None and task.completed != completed:
                continue
            if recurring is not None:
                is_recurring = task.frequency.lower() != "once"
                if is_recurring != recurring:
                    continue
            filtered.append((pet, task))
        return filtered

    def get_recurring_tasks(self, items: List[tuple[Pet, Task]] | None = None) -> List[tuple[Pet, Task]]:
        """Return tasks that repeat more than once."""
        return self.filter_tasks(items=items, recurring=True)

    def complete_task(self, pet: Pet, task: Task) -> None:
        """Mark a task complete and create the next recurring copy if needed."""
        task.mark_complete()
        if task.frequency.lower() != "once":
            next_task = Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                completed=False,
            )
            pet.add_task(next_task)

    def detect_conflicts(self, items: List[tuple[Pet, Task]] | None = None) -> List[str]:
        """Return lightweight warning messages for exact-time task conflicts."""
        schedule = items if items is not None else self.build_daily_schedule()
        warnings: List[str] = []
        seen: dict[int, tuple[Pet, Task]] = {}
        for item in schedule:
            pet, task = item
            key = self._time_to_minutes(task.time)
            if key in seen:
                previous_pet, previous_task = seen[key]
                warnings.append(
                    f"Warning: {previous_pet.name}'s '{previous_task.description}' and {pet.name}'s '{task.description}' share the same time of {task.time}."
                )
            else:
                seen[key] = item
        return warnings

    def print_schedule(self) -> str:
        """Return a readable daily schedule for the terminal."""
        lines = ["Today's Schedule"]
        for pet, task in self.build_daily_schedule():
            status = "Done" if task.completed else "Pending"
            lines.append(f"- {pet.name}: {task.description} at {task.time} ({status})")
        return "\n".join(lines)
