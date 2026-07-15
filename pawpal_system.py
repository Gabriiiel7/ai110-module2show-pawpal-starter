from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    time: str | None = None
    completed: bool = False

    def mark_done(self) -> None:
        self.completed = True

    def edit(self, title: str | None = None, duration_minutes: int | None = None,
             priority: str | None = None, time: str | None = None) -> None:
        if title is not None:
            self.title = title
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority
        if time is not None:
            self.time = time


@dataclass
class Pet:
    name: str
    species: str
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def update_info(self, name: str | None = None, species: str | None = None,
                    notes: str | None = None) -> None:
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
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


@dataclass
class Schedule:
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def build_plan(self) -> List[Task]:
        return sorted(self.tasks, key=lambda task: (task.priority != "high", task.time or ""))

    def explain_plan(self) -> str:
        if not self.tasks:
            return "No tasks planned."
        planned = ", ".join(task.title for task in self.tasks)
        return f"Planned tasks: {planned}"
