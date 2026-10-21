# BFS Visualizer — DAA GUI Implementation

An interactive, desktop-based GUI application developed for the **Design and Analysis of Algorithms (DAA)** B.Tech Computer Science course to demonstrate and visualize the **Breadth-First Search (BFS)** graph traversal algorithm.

Built purely using **Python 3** and **Tkinter**, this visualizer requires no external third-party dependencies, making it clean, lightweight, and easy to run on both Windows and Linux (Ubuntu).

---

## 📌 Project Overview

Breadth-First Search (BFS) is a fundamental graph traversal algorithm that explores vertices level by level using a **First-In, First-Out (FIFO) Queue**. Starting from a designated root node, it inspects all direct neighbors before progressing to vertices at the next depth level.

This project visualizes the algorithm on the predefined undirected graph:
- **Vertices (V):** `A, B, C, D, E, F, G, H`
- **Edges (E):** `A-B`, `A-C`, `B-D`, `B-E`, `C-F`, `C-G`, `E-H`

When executed starting at node **A**, the traversal produces the exact expected sequence:
$$\mathbf{A \rightarrow B \rightarrow C \rightarrow D \rightarrow E \rightarrow F \rightarrow G \rightarrow H}$$

---

## ✨ Features

- **Tkinter Canvas Graph Rendering:** Nodes are rendered as clearly labeled circles positioned in an intuitive hierarchical layout, connected by clean edge lines.
- **Color-Coded Node States:**
  - ⚪ **Unvisited:** Slate white / light grey (`#E2E8F0`)
  - 🟡 **In Queue (Discovered):** Amber gold (`#FBBF24`)
  - 🔴 **Currently Active (Processing):** Crimson red (`#EF4444`)
  - 🟢 **Visited (Completed):** Emerald green (`#22C55E`)
  - 🔵 **Active Edge:** Royal blue (`#3B82F6`)
- **Dual Execution Modes:**
  - **Run BFS / Pause / Resume:** Automated animation using Tkinter's non-blocking `root.after()` method.
  - **Next Step:** Discrete step-by-step execution using a Python generator (`yield`), ideal for viva and classroom demonstrations.
- **Interactive Start Node Selector:** Dropdown combobox to initiate BFS from any node (`A` through `H`).
- **Adjustable Animation Speed:** Interactive slider ranging from 300ms to 2000ms.
- **Live Algorithm Monitor:**
  - Displays the real-time content of the FIFO queue: `Front -> [ ... ] <- Rear`.
  - Shows the accumulated traversal sequence.
- **Dynamic Step Explanations:** Explains the exact algorithmic reason for every operation (enqueue, dequeue, neighbor inspection).
- **Asymptotic Complexity Card:** Direct summary of time and space complexity based on course lecture slides.

---

## 🗂 Project Structure

```text
daa-bfs-gui/
├── main.py        # Complete GUI and BFS algorithm implementation
└── README.md      # Documentation, setup guide, and complexity analysis
```

---

## 🚀 Installation & Execution Instructions

### Prerequisites
- Python 3.8 or higher installed.
- Tkinter installed (bundled with standard Python on Windows and macOS).

### 🖥️ Running on Windows
1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd path\to\daa-bfs-gui
   ```
3. Run the application:
   ```powershell
   python main.py
   ```

### 🐧 Running on Ubuntu / Linux
1. Open a terminal.
2. Ensure Python 3 and Tkinter are installed:
   ```bash
   sudo apt update
   sudo apt install python3 python3-tk -y
   ```
3. Navigate to the project directory:
   ```bash
   cd path/to/daa-bfs-gui
   ```
4. Run the application:
   ```bash
   python3 main.py
   ```

---

## 🧠 Algorithm & Pseudocode

Based directly on standard DAA curriculum lecture notes:

```text
Algorithm BFS (start_vertex)
1. Initialize all nodes by setting their flag to not visited (0)
2. Put the starting node into the queue and change its flag to visited (1)
3. while (queue is not empty) do:
    a. remove front node, N from queue (N = dequeue())
    b. process N (display N / append to traversal order)
    c. for each vertex v in G.Adj[N] do:
        if (visited[v] == 0) then:
            visited[v] = 1
            enqueue(v)
        end if
       end for
   end while
4. Stop
```

---

## 📊 Complexity Analysis

### 1. Time Complexity: $\mathcal{O}(V + E)$
- **Vertex Operations $\mathcal{O}(V)$:** Every vertex is marked visited and enqueued at most once, and dequeued at most once. Enqueue and dequeue operations with `collections.deque` take $\mathcal{O}(1)$ amortized time.
- **Edge Operations $\mathcal{O}(E)$:** When vertex $u$ is dequeued, its adjacency list $\text{Adj}[u]$ is scanned. Across the entire execution for all vertices, each edge in an undirected graph is inspected exactly twice (once from each endpoint):
  $$\sum_{u \in V} \text{deg}(u) = 2E \implies \mathcal{O}(E)$$
- **Total Running Time:** $\mathcal{O}(V + E)$.

### 2. Space Complexity: $\mathcal{O}(V)$
- **Queue Auxiliary Space:** In the worst-case scenario (e.g., a star graph or dense level), the FIFO queue holds up to $\mathcal{O}(V)$ vertices.
- **Visited Tracking & Adjacency List:** The visited set / array requires $\mathcal{O}(V)$ space.
- **Total Auxiliary Space:** $\mathcal{O}(V)$.

---

## 🔍 Code Walkthrough

1. **Adjacency List (`self.adj_list`):**
   A standard Python dictionary mapping each vertex to its list of adjacent neighbors. Represents the undirected graph without matrix overhead.
2. **FIFO Queue (`collections.deque`):**
   Provides $\mathcal{O}(1)$ push (`append()`) and $\mathcal{O}(1)$ pop from the front (`popleft()`), strictly conforming to FIFO queue requirements.
3. **Step Generator (`bfs_generator()`):**
   Uses Python's `yield` statement to divide the algorithm into discrete, pause-able execution states (enqueue start $\rightarrow$ dequeue node $\rightarrow$ examine each neighbor $\rightarrow$ finalize node).
4. **Non-Blocking Animation (`_auto_step()` & `root.after()`):**
   Schedules the next step without freezing the Tkinter event loop or requiring multi-threading complexity.
5. **Canvas Visual Elements (`self.canvas`):**
   Draws edges (`create_line`) and nodes (`create_oval` + `create_text`) with distinct tag references for color transitions.

---

## 🧪 Verification & Test Cases

| Test Case | Start Vertex | Expected Traversal Sequence | Status |
|---|---|---|---|
| **Test Case 1 (Primary)** | **A** | `A → B → C → D → E → F → G → H` | ✅ Passed |
| **Test Case 2** | **B** | `B → A → D → E → C → H → F → G` | ✅ Passed |
| **Test Case 3** | **C** | `C → A → F → G → B → D → E → H` | ✅ Passed |
| **Test Case 4** | **D** | `D → B → A → E → C → H → F → G` | ✅ Passed |
| **Test Case 5** | **E** | `E → B → H → A → D → C → F → G` | ✅ Passed |
| **Test Case 6** | **H** | `H → E → B → A → D → C → F → G` | ✅ Passed |

---

## 🎓 Faculty Evaluation / Viva Tips

- **Why use `collections.deque` instead of Python `list`?**
  Popping from the start of a list `list.pop(0)` is $\mathcal{O}(N)$ because all subsequent elements must be shifted in memory. `deque.popleft()` runs in $\mathcal{O}(1)$ constant time.
- **Why is BFS optimal for unweighted shortest paths?**
  Because BFS traverses nodes in order of their edge distance from the source vertex (level by level), the first time an unvisited node is reached is guaranteed to be via a shortest path in terms of edge count.
- **How does the GUI prevent duplicate node visits?**
  A node is marked as visited immediately upon being *enqueued* (not when dequeued), which prevents other vertices connected to it from enqueuing it a second time.
