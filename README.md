# 🧩 Zombie Puzzle KBS

This project implements a **Knowledge-Based System (KBS)** to solve the classic **Zombie Puzzle** using three different approaches:

* **Breadth-First Search (BFS)**
* **Depth-First Search (DFS)**
* **Forward Chaining (Rule-Based Inference)**

It is designed as a comparative study between **search-based algorithms** and **rule-based reasoning** for solving logical puzzles.
The project demonstrates how different AI paradigms approach the same problem and highlights their advantages and trade-offs.

---

## 📖 Problem Description

The **Zombie Puzzle** is a classic bridge-crossing challenge with a twist:

* A group of characters must cross a bridge at night.
* Only a limited number of people can cross at a time.
* They must use a torch to cross.
* Each person has a different crossing speed.
* If rules are not satisfied, zombies may appear as obstacles.

The objective is to find a **valid sequence of moves** to transfer everyone safely across the bridge under the constraints.

---

## ⚙️ Features

* **BFS Solver** → Guarantees the **shortest solution** if one exists.
* **DFS Solver** → Explores deep state spaces efficiently with lower memory.
* **Forward Chaining Solver** → Uses a **knowledge base** and **inference rules** to solve the puzzle in a human-like manner.
* **Layered architecture** with separation of:

  * `Engine` → Core puzzle logic and state representation.
  * `Facts` → Knowledge base (bridge, logs, visited states, etc.).
  * `Utils` → Helper functions (pretty printing, etc.).
* Provides **step-by-step solution output** for better visualization.

---

## 🗂 Project Structure

```
Zombie-Puzzle-KBS/
│── BFSSolver/                # Breadth-First Search solver
│   ├── Engine/               # Puzzle logic and state representation
│   ├── Facts/                # Knowledge (bridge, logs, visited states)
│   ├── Utils/                # Pretty printing and helpers
│   └── main.py               # Entry point for BFS solver
│
│── DFSSolver/                # Depth-First Search solver
│   ├── Engine/
│   ├── Facts/
│   ├── Utils/
│   └── main.py
│
│── ForwardChaining/          # Rule-based solver
│   ├── Engine/               # Rules and state transitions
│   ├── Facts/                # Knowledge base
│   └── main.py
│
│── .vscode/                  # VSCode settings
│── README.md                 # Project documentation
```

---

## 🔧 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Zombie-Puzzle-KBS.git
cd Zombie-Puzzle-KBS
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

Install dependencies (if required):

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run BFS Solver

```bash
python BFSSolver/main.py
```

### Run DFS Solver

```bash
python DFSSolver/main.py
```

### Run Forward Chaining Solver

```bash
python ForwardChaining/main.py
```

---

## 📊 Comparison Between Approaches

| Method               | Pros                                   | Cons                         |
| -------------------- | -------------------------------------- | ---------------------------- |
| **BFS**              | Guarantees shortest path               | Higher memory usage          |
| **DFS**              | Fast in small state spaces, low memory | May miss optimal solutions   |
| **Forward Chaining** | Human-like reasoning using rules       | Needs well-defined knowledge |

---

## 🎯 Educational Purpose

This project is intended as a **teaching and demonstration tool** for AI students and enthusiasts.
It helps illustrate:

* How **search algorithms** (BFS, DFS) traverse state spaces.
* How **knowledge-based systems** and **inference engines** operate.
* The trade-offs between **algorithmic search** and **symbolic reasoning**.

---

## 🤝 Contribution

Contributions are welcome!
Feel free to **fork this repo**, create a new branch, and submit a pull request with your improvements.

---

## 📜 License

This project is licensed under the **MIT License** – you are free to use, modify, and distribute it.

---

## 👨‍💻 Author

Developed by **\[MNourZureik]**
AI & Software Engineer

---
