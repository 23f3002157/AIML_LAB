The **Wumpus World problem** is a classic example from **artificial intelligence (AI)**, particularly in the field of **knowledge representation and reasoning**. It was introduced in the AI textbook by **Russell and Norvig** as a way to illustrate how an intelligent agent can make decisions in an uncertain, partially observable environment.

---

### 🧩 The Basic Idea

The **Wumpus World** is a simple, grid-based world (often a 4×4 grid) where an **agent** explores to find **gold** and avoid **hazards** like:

* **The Wumpus** — a monster that kills the agent if it enters its cell.
* **Pits** — deadly holes that also kill the agent.
* **Walls** — boundaries of the world.

The agent starts in a known position (e.g., the bottom-left cell), and must:

* **Find and grab the gold**,
* **Avoid being killed**, and
* **Escape safely** back to the starting point.

---

### 👃 Sensory Percepts

The agent cannot see the entire world — it perceives **clues** from nearby cells:

| Percept     | What it means                         |
| ----------- | ------------------------------------- |
| **Stench**  | There’s a Wumpus in an adjacent cell. |
| **Breeze**  | There’s a pit in an adjacent cell.    |
| **Glitter** | Gold is in the current cell.          |
| **Bump**    | The agent bumped into a wall.         |
| **Scream**  | The Wumpus has been killed.           |

The agent uses these **percepts** to infer what might be in neighboring squares.

---

### 🧠 The AI Challenge

The problem is a testbed for **logical inference and planning under uncertainty**.
The agent must reason like this:

> “I feel a breeze at (2,1), so at least one of (2,2) or (3,1) might contain a pit. But (3,1) had no breeze before, so the pit must be at (2,2).”

The agent builds a **knowledge base (KB)** and uses **propositional logic** or **first-order logic** to deduce safe and dangerous locations.

---

### 🎯 Goals of the Wumpus World Agent

1. **Grab the gold** (maximize reward).
2. **Avoid death** (avoid Wumpus and pits).
3. **Use reasoning** to make safe moves.
4. **Plan a path** back to the start and **exit**.

---

### 🧮 Representation Example

Each cell might have logical statements like:

* `Breeze(2,1) → Pit(2,2) ∨ Pit(3,1)`
* `¬Pit(3,1)` (no breeze was felt earlier)
* Therefore: `Pit(2,2)`

This logical reasoning helps the agent decide where to move safely.

---

### 💡 Why It’s Important

The Wumpus World problem demonstrates:

* **Knowledge-based agents** (using logic to act rationally)
* **Reasoning with uncertainty**
* **Planning and search in partially observable environments**
* The foundations of modern **AI reasoning systems** and **probabilistic inference**

---
