# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Add a pet – The user can enter a new pet's info (name, type, etc.) so the app knows about it.
Schedule a task – The user can set up a feeding, walk, medication, or appointment for a specific pet at a specific time.
View today's schedule – The user can see a simple list of everything that needs to happen today, across all their pets.

**Class brainstorm**

- Owner: Holds the owner's name and the list of pets.
- Owner: Can add a pet and see the daily plan.
- Pet: Holds the pet's name, species, and care notes.
- Pet: Can update its info and show its tasks.
- Task: Holds the task title, time, duration, and priority.
- Task: Can be scheduled, edited, or marked done.
- Schedule: Holds the date and the list of planned tasks.
- Schedule: Can sort tasks, build a plan, and explain why each task was chosen.

```mermaid
classDiagram
    class Owner {
        +String name
        +List~Pet~ pets
        +addPet()
        +viewPlan()
    }
    class Pet {
        +String name
        +String species
        +String notes
        +List~Task~ tasks
        +addTask()
        +updateInfo()
    }
    class Task {
        +String title
        +String time
        +int duration
        +String priority
        +editTask()
        +markDone()
    }
    class Schedule {
        +String date
        +List~Task~ tasks
        +buildPlan()
        +explainPlan()
    }
    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Schedule "1" --> "0..*" Task : includes
```

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
