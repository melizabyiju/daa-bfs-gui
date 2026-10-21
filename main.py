"""
BFS Visualizer - Breadth-First Search GUI Implementation
Design and Analysis of Algorithms (DAA) Assignment
B.Tech Computer Science and Engineering

Technology:
- Python 3
- Tkinter GUI & Canvas
- collections.deque for FIFO queue operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque


class BFSVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Visualizer - DAA Algorithm Visualizer")
        self.root.geometry("1020;720".replace(";", "x"))
        self.root.minsize(980, 680)
        self.root.configure(bg="#F4F6F9")

        # ---------------- Predefined Undirected Graph ----------------
        # Edges: A-B, A-C, B-D, B-E, C-F, C-G, E-H
        # Adjacency list representation
        self.adj_list = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F', 'G'],
            'D': ['B'],
            'E': ['B', 'H'],
            'F': ['C'],
            'G': ['C'],
            'H': ['E']
        }

        # Node coordinates on Canvas (x, y) designed for clean hierarchy & spacing
        self.node_positions = {
            'A': (380, 70),
            'B': (220, 170),
            'C': (540, 170),
            'D': (130, 290),
            'E': (310, 290),
            'F': (460, 290),
            'G': (620, 290),
            'H': (310, 400)
        }

        self.node_radius = 26

        # Color Palette
        self.COLOR_BG = "#F4F6F9"
        self.COLOR_PANEL = "#FFFFFF"
        self.COLOR_ACCENT = "#2563EB"       # Royal Blue
        self.COLOR_UNVISITED = "#E2E8F0"    # Crisp light gray
        self.COLOR_QUEUE = "#FBBF24"        # Amber / yellow (in queue / discovered)
        self.COLOR_CURRENT = "#EF4444"      # Crimson / Red (currently active / processing)
        self.COLOR_VISITED = "#22C55E"      # Green (completed / visited)
        self.COLOR_EDGE = "#94A3B8"         # Slate gray for default edges
        self.COLOR_EDGE_ACTIVE = "#3B82F6"  # Highlighted edge
        self.COLOR_TEXT = "#0F172A"         # Slate dark text

        # Animation state variables
        self.anim_job = None
        self.is_running = False
        self.step_generator = None
        self.animation_speed_ms = 900

        # Algorithm Tracking
        self.queue = deque()
        self.visited_set = set()
        self.traversal_order = []
        self.node_state = {node: "UNVISITED" for node in self.adj_list}
        self.edge_items = {}
        self.node_circle_items = {}
        self.node_text_items = {}

        # Build UI layout
        self._build_gui()

        # Initial graph render
        self.reset_graph()

    def _build_gui(self):
        """Constructs modern, responsive, cleanly partitioned Tkinter GUI."""
        # Top Header Banner
        header_frame = tk.Frame(self.root, bg="#1E293B", height=65)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="BFS Visualizer",
            font=("Segoe UI", 20, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        )
        title_lbl.pack(side=tk.LEFT, padx=22, pady=12)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Breadth-First Search Graph Traversal Animation",
            font=("Segoe UI", 11),
            fg="#94A3B8",
            bg="#1E293B"
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=5, pady=16)

        # Main Body Split: Left is Graph Canvas, Right is Control & Info Panel
        content_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # Left Container (Canvas + Legend)
        left_container = tk.Frame(content_frame, bg=self.COLOR_BG)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Canvas Frame
        canvas_card = tk.Frame(left_container, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        canvas_card.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_card,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Legend Bar at bottom of Canvas
        legend_frame = tk.Frame(left_container, bg="#FFFFFF", bd=1, relief=tk.SOLID, height=44)
        legend_frame.pack(fill=tk.X, pady=(8, 0))

        legends = [
            ("Unvisited", self.COLOR_UNVISITED, "#64748B"),
            ("Enqueued (In Queue)", self.COLOR_QUEUE, "#B45309"),
            ("Current Active (Dequeued)", self.COLOR_CURRENT, "#B91C1C"),
            ("Fully Visited", self.COLOR_VISITED, "#15803D"),
        ]
        tk.Label(legend_frame, text="Legend:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(side=tk.LEFT, padx=(12, 8), pady=8)
        for label_text, color, border in legends:
            item_box = tk.Canvas(legend_frame, width=16, height=16, bg="#FFFFFF", highlightthickness=0)
            item_box.pack(side=tk.LEFT, padx=(6, 2))
            item_box.create_oval(2, 2, 14, 14, fill=color, outline=border, width=1.5)
            tk.Label(legend_frame, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF", fg="#475569").pack(side=tk.LEFT, padx=(0, 12))

        # Right Control & State Panel
        right_panel = tk.Frame(content_frame, bg=self.COLOR_BG, width=380)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_panel.pack_propagate(False)

        # Card 1: Controls
        ctrl_card = tk.LabelFrame(
            right_panel,
            text=" Traversal Controls ",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=14,
            pady=12,
            relief=tk.GROOVE
        )
        ctrl_card.pack(fill=tk.X, pady=(0, 10))

        # Start Node Selection
        start_row = tk.Frame(ctrl_card, bg="#FFFFFF")
        start_row.pack(fill=tk.X, pady=(0, 10))

        tk.Label(start_row, text="Start Node:", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155").pack(side=tk.LEFT)

        self.start_node_var = tk.StringVar(value="A")
        node_options = sorted(list(self.adj_list.keys()))
        self.node_dropdown = ttk.Combobox(
            start_row,
            textvariable=self.start_node_var,
            values=node_options,
            state="readonly",
            width=8,
            font=("Segoe UI", 10)
        )
        self.node_dropdown.pack(side=tk.RIGHT, padx=4)
        self.node_dropdown.bind("<<ComboboxSelected>>", self.on_start_node_changed)

        # Speed Slider
        speed_row = tk.Frame(ctrl_card, bg="#FFFFFF")
        speed_row.pack(fill=tk.X, pady=(0, 10))
        tk.Label(speed_row, text="Anim Speed:", font=("Segoe UI", 9), bg="#FFFFFF", fg="#475569").pack(side=tk.LEFT)
        self.speed_slider = tk.Scale(
            speed_row,
            from_=300,
            to=2000,
            resolution=100,
            orient=tk.HORIZONTAL,
            showvalue=False,
            bg="#FFFFFF",
            troughcolor="#E2E8F0",
            highlightthickness=0,
            command=self._update_speed
        )
        self.speed_slider.set(900)
        self.speed_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=6)

        # Button Row
        btn_grid = tk.Frame(ctrl_card, bg="#FFFFFF")
        btn_grid.pack(fill=tk.X)

        self.btn_run = tk.Button(
            btn_grid,
            text="▶ Run BFS",
            command=self.run_bfs,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=6
        )
        self.btn_run.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_step = tk.Button(
            btn_grid,
            text="⏭ Next Step",
            command=self.step_bfs,
            bg="#0D9488",
            fg="white",
            activebackground="#0F766E",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=6
        )
        self.btn_step.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_reset = tk.Button(
            btn_grid,
            text="↺ Reset",
            command=self.reset_graph,
            bg="#64748B",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=6
        )
        self.btn_reset.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Card 2: Algorithm Live Monitor (Queue + Traversal)
        monitor_card = tk.LabelFrame(
            right_panel,
            text=" Live Algorithm State ",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=14,
            pady=10,
            relief=tk.GROOVE
        )
        monitor_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(monitor_card, text="Current Queue [FIFO]:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(anchor=tk.W)
        self.queue_disp = tk.Label(
            monitor_card,
            text="[ Empty ]",
            font=("Consolas", 11, "bold"),
            bg="#F1F5F9",
            fg="#1E293B",
            relief=tk.RIDGE,
            padx=8,
            pady=6,
            anchor=tk.W
        )
        self.queue_disp.pack(fill=tk.X, pady=(3, 8))

        tk.Label(monitor_card, text="Traversal Order:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(anchor=tk.W)
        self.order_disp = tk.Label(
            monitor_card,
            text="(None)",
            font=("Consolas", 11, "bold"),
            bg="#F1F5F9",
            fg="#0F766E",
            relief=tk.RIDGE,
            padx=8,
            pady=6,
            anchor=tk.W,
            wraplength=330,
            justify=tk.LEFT
        )
        self.order_disp.pack(fill=tk.X, pady=(3, 4))

        # Card 3: Step Explanation
        exp_card = tk.LabelFrame(
            right_panel,
            text=" Step Explanation ",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=14,
            pady=10,
            relief=tk.GROOVE
        )
        exp_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.step_desc = tk.Text(
            exp_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            fg="#1E293B",
            wrap=tk.WORD,
            height=5,
            bd=0,
            relief=tk.FLAT
        )
        self.step_desc.pack(fill=tk.BOTH, expand=True)
        self.step_desc.insert(tk.END, "Ready. Select a starting node and click 'Run BFS' or 'Next Step'.")
        self.step_desc.configure(state="disabled")

        # Card 4: Asymptotic Complexity Analysis
        comp_card = tk.LabelFrame(
            right_panel,
            text=" Complexity Analysis ",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=14,
            pady=8,
            relief=tk.GROOVE
        )
        comp_card.pack(fill=tk.X)

        t_lbl = tk.Label(
            comp_card,
            text="• Time Complexity:  O(V + E)\n  Every vertex is queued once O(V), and each adjacency\n  list edge is scanned once O(E).",
            font=("Segoe UI", 8),
            justify=tk.LEFT,
            bg="#FFFFFF",
            fg="#334155"
        )
        t_lbl.pack(anchor=tk.W, pady=(0, 4))

        s_lbl = tk.Label(
            comp_card,
            text="• Space Complexity: O(V)\n  Queue and visited structures store at most V vertices.",
            font=("Segoe UI", 8),
            justify=tk.LEFT,
            bg="#FFFFFF",
            fg="#334155"
        )
        s_lbl.pack(anchor=tk.W)

    def _update_speed(self, val):
        self.animation_speed_ms = int(val)

    def _draw_initial_graph(self):
        """Draws static graph layout with labeled circular nodes and edges."""
        self.canvas.delete("all")
        self.edge_items.clear()
        self.node_circle_items.clear()
        self.node_text_items.clear()

        # Draw all edges first so they sit beneath node circles
        drawn_edges = set()
        for u in self.adj_list:
            for v in self.adj_list[u]:
                edge_key = tuple(sorted([u, v]))
                if edge_key not in drawn_edges:
                    drawn_edges.add(edge_key)
                    x1, y1 = self.node_positions[u]
                    x2, y2 = self.node_positions[v]
                    line_id = self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=self.COLOR_EDGE,
                        width=2.5,
                        capstyle=tk.ROUND
                    )
                    self.edge_items[edge_key] = line_id

        # Draw nodes (circles + text labels)
        r = self.node_radius
        for node, (x, y) in self.node_positions.items():
            circle_id = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.COLOR_UNVISITED,
                outline="#94A3B8",
                width=2
            )
            text_id = self.canvas.create_text(
                x, y,
                text=node,
                font=("Segoe UI", 12, "bold"),
                fill=self.COLOR_TEXT
            )
            self.node_circle_items[node] = circle_id
            self.node_text_items[node] = text_id

    def set_node_color(self, node, fill_color, outline_color=None, text_color=None):
        """Helper to style node circle and label."""
        if node in self.node_circle_items:
            kw = {"fill": fill_color}
            if outline_color:
                kw["outline"] = outline_color
            self.canvas.itemconfig(self.node_circle_items[node], **kw)
        if text_color and node in self.node_text_items:
            self.canvas.itemconfig(self.node_text_items[node], fill=text_color)

    def highlight_edge(self, u, v, active=True):
        """Highlight edge connecting u and v during discovery."""
        edge_key = tuple(sorted([u, v]))
        if edge_key in self.edge_items:
            color = self.COLOR_EDGE_ACTIVE if active else self.COLOR_EDGE
            width = 3.5 if active else 2.5
            self.canvas.itemconfig(self.edge_items[edge_key], fill=color, width=width)

    def update_explanation(self, text):
        """Displays formatted message in the Step Explanation box."""
        self.step_desc.configure(state="normal")
        self.step_desc.delete("1.0", tk.END)
        self.step_desc.insert(tk.END, text)
        self.step_desc.configure(state="disabled")

    def update_displays(self):
        """Updates FIFO Queue display and Traversal string."""
        if self.queue:
            q_str = "Front -> [ " + ", ".join(self.queue) + " ] <- Rear"
        else:
            q_str = "[ Empty ]"
        self.queue_disp.config(text=q_str)

        if self.traversal_order:
            self.order_disp.config(text=" → ".join(self.traversal_order))
        else:
            self.order_disp.config(text="(None)")

    def on_start_node_changed(self, event=None):
        """Handles user selecting a different start node from the dropdown."""
        if self.is_running:
            self.stop_animation()
        self.reset_graph()

    def reset_graph(self):
        """Restores the initial graph state, resets collections, and clears UI displays."""
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.is_running = False

        self.queue.clear()
        self.visited_set.clear()
        self.traversal_order.clear()
        self.step_generator = None

        self.node_dropdown.config(state="readonly")
        self.btn_run.config(text="▶ Run BFS", state="normal")
        self.btn_step.config(state="normal")

        self._draw_initial_graph()
        self.update_displays()
        start = self.start_node_var.get()
        self.update_explanation(
            f"Graph reset. Start node set to '{start}'.\nClick 'Run BFS' for automatic animation or 'Next Step' to step manually."
        )

    def bfs_generator(self, start_node):
        """
        Generator yielding each discrete BFS step for animation / stepping.
        Follows standard DAA BFS algorithm:
        1. Initialize all nodes as unvisited (flag = 0).
        2. Put starting node into queue and mark visited (flag = 1).
        3. While queue is not empty:
            a. Dequeue front node N.
            b. Process / Display N.
            c. For each unvisited neighbor v in Adj[N]:
                - Mark visited (flag = 1)
                - Enqueue v
        """
        # Step 1: Initializing start node
        self.visited_set.add(start_node)
        self.queue.append(start_node)
        self.set_node_color(start_node, self.COLOR_QUEUE, outline_color="#B45309", text_color="#78350F")
        self.update_displays()
        yield (
            f"Step 1: Enqueue start node '{start_node}' and set visited flag = 1.\n"
            f"Queue now contains [{start_node}]."
        )

        # Step 2: Queue processing loop
        while self.queue:
            # Current front node
            current = self.queue.popleft()
            self.traversal_order.append(current)
            self.set_node_color(current, self.COLOR_CURRENT, outline_color="#991B1B", text_color="#FFFFFF")
            self.update_displays()

            yield (
                f"Processing Node '{current}': Dequeued front node.\n"
                f"Added '{current}' to traversal output order.\n"
                f"Examining adjacent vertices in Adj[{current}]: {self.adj_list.get(current, [])}."
            )

            # Examine adjacent vertices
            neighbors = self.adj_list.get(current, [])
            discovered_any = False

            for neighbor in neighbors:
                if neighbor not in self.visited_set:
                    discovered_any = True
                    self.visited_set.add(neighbor)
                    self.queue.append(neighbor)
                    self.highlight_edge(current, neighbor, active=True)
                    self.set_node_color(neighbor, self.COLOR_QUEUE, outline_color="#B45309", text_color="#78350F")
                    self.update_displays()
                    yield (
                        f"Neighbor '{neighbor}' is unvisited:\n"
                        f"Set visited flag = 1, enqueue '{neighbor}', highlight edge ({current}, {neighbor})."
                    )

            if not discovered_any:
                yield f"No unvisited neighbors remaining for node '{current}'."

            # Mark current as fully completed / visited
            self.set_node_color(current, self.COLOR_VISITED, outline_color="#166534", text_color="#FFFFFF")
            self.update_displays()
            yield f"Finished processing node '{current}'. Marked as fully visited."

        # Verification of disconnected nodes
        all_nodes = set(self.adj_list.keys())
        unvisited_remaining = all_nodes - self.visited_set
        if unvisited_remaining:
            yield (
                f"BFS Complete for component rooted at '{start_node}'.\n"
                f"Note: Unreachable/disconnected vertices: {sorted(list(unvisited_remaining))}."
            )
        else:
            yield (
                f"BFS Traversal Complete!\n"
                f"All {len(self.visited_set)} reachable nodes processed.\n"
                f"Final Order: {' → '.join(self.traversal_order)}"
            )

    def step_bfs(self):
        """Advances BFS by exactly one discrete step."""
        if not self.step_generator:
            start_node = self.start_node_var.get()
            self.node_dropdown.config(state="disabled")
            self.step_generator = self.bfs_generator(start_node)

        try:
            explanation = next(self.step_generator)
            self.update_explanation(explanation)
            return True
        except StopIteration:
            self.is_running = False
            self.btn_run.config(text="▶ Run BFS", state="disabled")
            self.btn_step.config(state="disabled")
            return False

    def run_bfs(self):
        """Starts or pauses automated execution using Tkinter's non-blocking after() method."""
        if self.is_running:
            # If already running, allow pausing
            self.stop_animation()
            self.btn_run.config(text="▶ Resume BFS")
            return

        self.is_running = True
        self.btn_run.config(text="⏸ Pause BFS")
        self._auto_step()

    def _auto_step(self):
        """Internal recursive timer callback."""
        if not self.is_running:
            return

        has_next = self.step_bfs()
        if has_next:
            self.anim_job = self.root.after(self.animation_speed_ms, self._auto_step)
        else:
            self.anim_job = None
            self.is_running = False

    def stop_animation(self):
        """Pauses the automatic animation loop."""
        self.is_running = False
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None


def main():
    root = tk.Tk()
    app = BFSVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
