# simulatore.py

import tkinter as tk
from tkinter import ttk
import threading
import time
from bel_zab import BelZab
from random_generator import RandomGenerator

class Simulatore:
    def __init__(self, root):
        self.root = root
        self.root.title("SimulatoreInicio")
        self.dimension = 200
        self.alfa = 1.0
        self.beta = 1.0
        self.gamma = 1.0
        self.simulation_running = False
        self.create_widgets()

    def create_widgets(self):
        # Input fields and labels
        self.dimension_label = ttk.Label(self.root, text="Dimension:")
        self.dimension_entry = ttk.Entry(self.root)
        self.dimension_entry.insert(0, "200")

        self.alfa_label = ttk.Label(self.root, text="α (alfa):")
        self.alfa_entry = ttk.Entry(self.root)
        self.alfa_entry.insert(0, "1.0")

        self.beta_label = ttk.Label(self.root, text="β (beta):")
        self.beta_entry = ttk.Entry(self.root)
        self.beta_entry.insert(0, "1.0")

        self.gamma_label = ttk.Label(self.root, text="γ (gamma):")
        self.gamma_entry = ttk.Entry(self.root)
        self.gamma_entry.insert(0, "1.0")

        # Buttons
        self.create_sim_button = ttk.Button(self.root, text="Create Simulation", command=self.create_simulation)
        self.start_sim_button = ttk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.stop_sim_button = ttk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)

        # Layout
        self.dimension_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.dimension_entry.grid(row=0, column=1, padx=5, pady=5)

        self.alfa_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.alfa_entry.grid(row=1, column=1, padx=5, pady=5)

        self.beta_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.beta_entry.grid(row=2, column=1, padx=5, pady=5)

        self.gamma_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.gamma_entry.grid(row=3, column=1, padx=5, pady=5)

        self.create_sim_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.start_sim_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.stop_sim_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def create_simulation(self):
        # Get parameters from entries
        try:
            self.dimension = int(self.dimension_entry.get())
            self.alfa = float(self.alfa_entry.get())
            self.beta = float(self.beta_entry.get())
            self.gamma = float(self.gamma_entry.get())
        except ValueError:
            tk.messagebox.showerror("Invalid input", "Please enter valid numerical values.")
            return

        # Create simulation window
        self.simulation_window = tk.Toplevel(self.root)
        self.simulation_window.title("Simulation")
        self.canvas = tk.Canvas(self.simulation_window, width=self.dimension, height=self.dimension)
        self.canvas.pack()

        # Initialize the automaton
        self.automata = BelZab(self.dimension, self.alfa, self.beta, self.gamma)
        self.image = tk.PhotoImage(width=self.dimension, height=self.dimension)
        self.canvas.create_image((self.dimension / 2, self.dimension / 2), image=self.image, state="normal")

    def start_simulation(self):
        if not hasattr(self, 'automata'):
            tk.messagebox.showwarning("Simulation not created", "Please create the simulation first.")
            return

        if self.simulation_running:
            return  # Already running

        self.simulation_running = True
        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.daemon = True  # Allows thread to exit when main program exits
        self.simulation_thread.start()

    def stop_simulation(self):
        self.simulation_running = False

    def run_simulation(self):
        while self.simulation_running:
            self.automata.nextGen()
            self.update_canvas()

    def update_canvas(self):
        # Update the canvas with the new automata state
        p = self.automata.p
        for y in range(self.dimension):
            for x in range(self.dimension):
                # Get the RGB values based on the automata's state
                r = int(self.automata.a[x][y][p] * 255)
                g_val = int(self.automata.b[x][y][p] * 255)
                b = int(self.automata.c[x][y][p] * 255)
                color = f'#{r:02x}{g_val:02x}{b:02x}'
                self.image.put(color, (x, y))
        self.canvas.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = Simulatore(root)
    root.mainloop()
