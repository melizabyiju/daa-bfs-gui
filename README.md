# BFS Visualizer — DAA GUI Implementation

[![GitHub Pages](https://img.shields.io/badge/Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://melizabyiju.github.io/daa-bfs-gui/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An interactive, desktop and web-based graphical visualizer developed for the **Design and Analysis of Algorithms (DAA)** B.Tech Computer Science course to illustrate the **Breadth-First Search (BFS)** graph traversal algorithm.

---

## 🌐 Live Web Demo (GitHub Pages)

You can run and interact with the visualizer directly in any web browser without installing anything:

👉 **[Launch Live BFS Visualizer on GitHub Pages](https://melizabyiju.github.io/daa-bfs-gui/)**

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

- **Dual-Platform Availability:**
  - **Desktop GUI:** Native desktop application powered by **Python 3 & Tkinter Canvas**.
  - **Web GUI (GitHub Pages):** Responsive, interactive HTML5 / SVG / CSS / Vanilla JavaScript implementation with zero dependencies.
- **Color-Coded Node States:**
  - ⚪ **Unvisited:** Slate white / light grey (`#E2E8F0`)
  - 🟡 **In Queue (Discovered):** Amber gold (`#FBBF24`)
  - 🔴 **Currently Active (Processing):** Crimson red (`#EF4444`)
  - 🟢 **Visited (Completed):** Emerald green (`#22C55E`)
  - 🔵 **Active Edge:** Royal blue (`#2563EB`)
- **Dual Execution Modes:**
  - **Run BFS / Pause / Resume:** Automated animation using non-blocking timers (`root.after()` in Tkinter, `setTimeout()` in JS).
  - **Next Step:** Discrete step-by-step execution using Python & JavaScript generator functions (`yield`), ideal for faculty viva and classroom evaluation.
- **Interactive Start Node Selector:** Dropdown to initiate BFS from any node (`A` through `H`).
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
├── index.html     # Web version for GitHub Pages deployment (HTML5, SVG, Vanilla JS)
├── main.py        # Desktop GUI implementation (Python 3, Tkinter)
├── README.md      # Project documentation, algorithms, and complexity guide
└── .gitignore     # Git ignore configuration
```

---

## 🚀 Installation & Execution Instructions

### Option 1: Live in Browser (Recommended)
Visit the GitHub Pages deployment:
🔗 **[https://melizabyiju.github.io/daa-bfs-gui/](https://melizabyiju.github.io/daa-bfs-gui/)**

### Option 2: Desktop Python Application

#### Prerequisites
- Python 3.8 or higher installed.
- Tkinter installed (bundled with standard Python on Windows and macOS).

#### 🖥️ Windows (PowerShell / Command Prompt)
```powershell
# Clone the repository
git clone https://github.com/melizabyiju/daa-bfs-gui.git
cd daa-bfs-gui

# Run the desktop visualizer
python main.py
```

#### 🐧 Ubuntu / Debian Linux
```bash
# Update and install python3-tk
sudo apt update
sudo apt install python3 python3-tk -y

# Clone and run
git clone https://github.com/melizabyiju/daa-bfs-gui.git
cd daa-bfs-gui
python3 main.py
```

---

## 🧠 Algorithm & Pseudocode

Based directly on DAA curriculum lecture notes:

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
- **Vertex Operations $\mathcal{O}(V)$:** Every vertex is marked visited and enqueued at most once, and dequeued at most once. Enqueue and dequeue operations take $\mathcal{O}(1)$ time.
- **Edge Operations $\mathcal{O}(E)$:** When vertex $u$ is dequeued, its adjacency list $\text{Adj}[u]$ is scanned. Across the entire execution for all vertices, each edge in an undirected graph is inspected exactly twice (once from each endpoint):
  $$\sum_{u \in V} \text{deg}(u) = 2E \implies \mathcal{O}(E)$$
- **Total Running Time:** $\mathcal{O}(V + E)$.

### 2. Space Complexity: $\mathcal{O}(V)$
- **Queue Auxiliary Space:** In the worst-case scenario, the FIFO queue holds up to $\mathcal{O}(V)$ vertices.
- **Visited Tracking:** The visited set / flag array requires $\mathcal{O}(V)$ space.
- **Total Auxiliary Space:** $\mathcal{O}(V)$.

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

## ⚙️ Enabling GitHub Pages on Your Repository

1. Go to your repository settings:  
   `https://github.com/melizabyiju/daa-bfs-gui/settings/pages`
2. Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
3. Select branch **`main`** and folder **`/ (root)`**, then click **Save**.
4. Within 1–2 minutes, your live visualizer will be live at:  
   👉 `https://melizabyiju.github.io/daa-bfs-gui/`
