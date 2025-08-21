## @package chart
#  The chart module provides a class for plotting the health status of the population over time.
#  It uses matplotlib to create a visual representation of the simulation data.

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

class Chart(tk.Frame):
    ##
    # Initializes the Chart class.
    # This class creates a matplotlib figure and axes for plotting the health status of the population.
    # @param master: The parent widget for the chart.
    def __init__(
            self,
            master: tk.Misc,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.figure = Figure(figsize=(5,4), dpi = 100)
        self.ax = self.figure.add_subplot()
        self.ax.set_title('Outbreak Over Time')
        self.ax.set_xlabel('Time (days)')
        self.ax.set_ylabel('Number of People')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    ##
    # Plots the health status history on the chart.
    # This method clears the previous plot and draws the new data for susceptible, infected, and recovered individuals.
    # @param s_history: List of susceptible individuals over time.
    # @param i_history: List of infected individuals over time.
    # @param r_history: List of recovered individuals over time.
    # @return: A list containing the health status history.
    def plot(self, s_history, i_history, r_history):
        # Clear the previous plot
        self.ax.cla()

        # Prepare the axes labels & title again (since cla() wipes them):
        self.ax.set_title("Outbreak Over Time")
        self.ax.set_xlabel("Time (days)")
        self.ax.set_ylabel("Number of People")
        if not s_history or not i_history or not r_history:
            self.canvas.draw()
            return

        print("Plotting history at day:", max(range(len(s_history))))
        # Extract data from history
        times = list(range(len(s_history)))
        susceptible = s_history
        infected = i_history
        recovered = r_history
        # Plot the data
        self.ax.plot(times, susceptible, label='Susceptible', marker='')
        self.ax.plot(times, infected, label='Infected', marker='')
        self.ax.plot(times, recovered, label='Recovered', marker='')
        self.ax.legend(loc='upper right')
        self.ax.grid()
        self.canvas.draw()
        return [s_history, i_history, r_history]