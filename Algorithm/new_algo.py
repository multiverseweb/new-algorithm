'''
Design and Analysis of Algorithms
Project Based Learning

Project Name: Hybrid Algorithm (Combining A* and Bellman–Ford Algorithm)

Submitted By:
Tejas Gupta - 2214110069
Ojas Gupta - 2214110070

Project guide: Dr. Bindu Garg
'''
#==============================================================================================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import time

class Algorithm:
    def __init__(self, graph, heuristic):
        self.graph = graph
        self.heuristic = heuristic

    def search(self, start, goal):
        # Initialize priority queue and costs
        priority_queue = []
        heapq.heappush(priority_queue, (0, start))
        g_score = {node: float('inf') for node in self.graph}
        f_score = {node: float('inf') for node in self.graph}
        g_score[start] = 0
        f_score[start] = self.heuristic(start, goal)
        previous = {}

        # Run |V| - 1 iterations to ensure all edges are relaxed
        for _ in range(len(self.graph) - 1):
            if not priority_queue:
                break
            _, current = heapq.heappop(priority_queue)

            # If goal is reached, construct the path
            if current == goal:
                return self.update_path(previous, current)

            for neighbor, weight in self.graph.get(current, []):
                temp_score = g_score[current] + weight
                if temp_score < g_score[neighbor]:
                    previous[neighbor] = current
                    g_score[neighbor] = temp_score
                    f_score[neighbor] = temp_score + self.heuristic(neighbor, goal)
                    heapq.heappush(priority_queue, (f_score[neighbor], neighbor))

        # Check for negative-weight cycles
        for node in self.graph:
            for neighbor, weight in self.graph.get(node, []):
                if g_score[node] != float('inf') and g_score[node] + weight < g_score[neighbor]:
                    return f"Graph contains a negative-weight cycle"

        return f"No path exists between {start} and {goal}."

    def update_path(self, previous, current):
        path = [current]
        while current in previous:
            current = previous[current]
            path.append(current)
        path.reverse()
        return path

#heuristic function (Manhattan Distance)
def heuristic(node, goal):
    return abs(node - goal)

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Algorithm (Bellman-Ford and A* Algorithm)")
        self.graph = {}
        self.nodes = []

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.heading = tk.Label(self.main_frame, text="Design and Analysis of Algorithms\nProject Based Learning", font=('Arial', 20))
        self.heading.grid(row=0, column=1, padx=5, pady=5)

        self.title_label = tk.Label(self.main_frame, text="Bellman-Ford and A* Algorithm\n(Hybrid Path Finding Algorithm)", font=('Arial', 20))
        self.title_label.grid(row=1, column=5, padx=5, pady=50)

        self.node_count_label = tk.Label(self.main_frame, text="Number of nodes:", font=('Arial', 12))
        self.node_count_label.grid(row=2, column=0, padx=20, pady=5)
        self.node_count_entry = tk.Entry(self.main_frame, font=('Arial', 12))
        self.node_count_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.generate_button = tk.Button(self.main_frame, text="Generate Graph", command=self.generate_graph, font=('Arial', 12))
        self.generate_button.grid(row=2, column=2, padx=5, pady=5)
        
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.canvas = tk.Canvas(self.main_frame, width=800, height=0, bg='white')
        self.canvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.update_button = tk.Button(self.main_frame, text="Update Graph", command=self.update_graph, font=('Arial', 12))
        self.update_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.source_label = tk.Label(self.main_frame, text="Source:         ", font=('Arial', 12))
        self.source_label.grid(row=5, column=1, padx=0, pady=5, sticky=tk.W)
        self.source_entry = tk.Entry(self.main_frame, font=('Arial', 12))
        self.source_entry.grid(row=5, column=1, padx=5, pady=5)
        
        self.goal_label = tk.Label(self.main_frame, text="Goal:  ", font=('Arial', 12))
        self.goal_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.goal_entry = tk.Entry(self.main_frame, font=('Arial', 12))
        self.goal_entry.grid(row=5, column=2, padx=5, pady=5)
        
        self.find_path_button = tk.Button(self.main_frame, text="Find Path", command=self.find_path, font=('Arial', 12))
        self.find_path_button.grid(row=6, column=1, columnspan=3, padx=5, pady=5)

        self.path_label = tk.Label(self.main_frame, text="Path:", font=('Arial', 12))
        self.path_label.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.path_display = tk.Text(self.main_frame, height=2, width=50, font=('Arial', 12))
        self.path_display.grid(row=7, column=1, columnspan=2, padx=5, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title("Graph Visualisation")
        self.ax.axis('off')
        self.canvas_figure = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas_figure.get_tk_widget().grid(row=2, column=5, rowspan=6, padx=5, pady=5, sticky=tk.NSEW)

    def generate_graph(self):
        self.graph.clear()
        self.nodes.clear()
        self.canvas.delete("all")
        self.clear_table()

        node_count = int(self.node_count_entry.get())
        self.nodes = list(range(node_count))

        for i in self.nodes:
            self.graph[i] = []
        
        for node in self.nodes:
            for _ in range(random.randint(1, 3)):
                neighbour = random.choice(self.nodes)
                if neighbour != node and neighbour not in [n for n, _ in self.graph[node]]:
                    weight = random.randint(1, 10)
                    self.graph[node].append((neighbour, weight))

        self.create_table()
        self.draw_graph()
        
    def create_table(self):
        self.clear_table()

        tk.Label(self.table_frame, text="Node", font=('Arial', 12)).grid(row=0, column=0)
        tk.Label(self.table_frame, text="Neighbor", font=('Arial', 12)).grid(row=0, column=1)
        tk.Label(self.table_frame, text="Weight", font=('Arial', 12)).grid(row=0, column=2)

        self.entries = {}
        for i, node in enumerate(self.nodes):
            tk.Label(self.table_frame, text=f"{node}", font=('Arial', 12)).grid(row=i+1, column=0)
            neighbor_entry = tk.Entry(self.table_frame, font=('Arial', 12))
            neighbor_entry.grid(row=i+1, column=1)
            weight_entry = tk.Entry(self.table_frame, font=('Arial', 12))
            weight_entry.grid(row=i+1, column=2)
            self.entries[node] = (neighbor_entry, weight_entry)
            self.update_entry(node)

    def update_entry(self, node):
        neighbors = self.graph.get(node, [])
        neighbor_str = ', '.join(str(n) for n, _ in neighbors)
        weight_str = ', '.join(str(w) for _, w in neighbors)
        neighbor_entry, weight_entry = self.entries[node]
        neighbor_entry.delete(0, tk.END)
        neighbor_entry.insert(0, neighbor_str)
        weight_entry.delete(0, tk.END)
        weight_entry.insert(0, weight_str)

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def update_graph(self):
        new_graph = {}
        for node, (neighbor_entry, weight_entry) in self.entries.items():
            # Get and sanitize input
            neighbors = neighbor_entry.get().strip().split(',')
            weights = weight_entry.get().strip().split(',')
            
            # Check if the lengths match and all entries are valid integers
            if len(neighbors) != len(weights):
                messagebox.showerror("Error", f"Number of neighbors and weights must match for node {node}.")
                return

            try:
                new_graph[node] = [
                    (int(neighbor.strip()), int(weight.strip()))
                    for neighbor, weight in zip(neighbors, weights)
                    if neighbor.strip() and weight.strip()
                ]
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for node {node}. Please ensure all neighbors and weights are integers.")
                return

        self.graph = new_graph
        self.draw_graph()


    def draw_graph(self):
        self.ax.clear()
        G = nx.DiGraph()
        for node in self.graph:
            for neighbour, weight in self.graph[node]:
                G.add_edge(node, neighbour, weight=weight)
                
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", ax=self.ax, font_size=10, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=self.ax)
        self.canvas_figure.draw()
        
    def find_path(self):
        try:
            source = int(self.source_entry.get().strip())
            goal = int(self.goal_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid source or goal node.")
            return

        if source not in self.graph or goal not in self.graph:
            messagebox.showerror("Error", "Source or goal node not in graph.")
            return

        algorithm = Algorithm(self.graph, heuristic)
        path = algorithm.search(source, goal)
        
        if not isinstance(path, list):
            messagebox.showerror("Error", path)
            return
        
        # Path text box
        self.path_display.delete(1.0, tk.END)
        self.path_display.insert(tk.END, " -> ".join(map(str, path)))

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()