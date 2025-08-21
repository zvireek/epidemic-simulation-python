## @package app
#  The main application class that initializes the simulation and visualizer.
#  It sets up the main window and starts the application loop.

import tkinter as tk

from simulation import Simulation
from gui import Visualizer


class App:
    ##
    # Initializes the main application.
    # This sets up the simulation and visualizer, and configures the main window.
    def __init__(self):
        self.simulation = Simulation()
        self.master = tk.Tk()
        self.visualizer = Visualizer(self.master, self.simulation)
        self.window_setup()

    ##
    # Sets up the main window for the application.
    # This includes setting the window size, title, and resizability.
    def window_setup(self):
        self.master.geometry("1600x800")
        self.master.title("Simulation by Jan Zurek")
        self.master.resizable(True, True)

    ##
    # Starts the main application loop.
    def start(self):
        self.master.mainloop()



if __name__ == "__main__":
    app = App()
    app.start()
