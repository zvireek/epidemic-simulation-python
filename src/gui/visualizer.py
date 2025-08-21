## @package visualizer
#  The main visualizer class that integrates the control panel, parameter panel, and chart.
#  It handles the simulation setup, running, and visualization of results.
#  This class is responsible for creating the GUI and managing user interactions.
#  It provides methods to start the simulation, step through it, and reset the state.

import tkinter as tk
from .controlpanel import ControlPanel
from .parameterpanel import ParameterPanel, SimulationParameters
from .chart import Chart


class Visualizer(tk.Frame):
    ##
    # Initializes the visualizer with the main window, simulation instance,
    # and sets up the control panel, parameter panel, and chart.
    # @param master: The main window or parent widget for the visualizer.
    # @param simulation: An instance of the Simulation class to be visualized.
    def __init__(
            self,
            master: tk.Misc,
            simulation,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.simulation = simulation
        self.paramPanel = ParameterPanel(master = master)
        self.controlPanel = ControlPanel(
            master = self.master,
            start_simulation = self.start_simulation,
            on_step = self.on_step,
            reset_simulation = self.reset_everything,
            toggle_social_distancing = self.simulation.toggle_social_distancing
        )
        self.chart = Chart(
            master = self.master
        )

        self.paramPanel.pack(side=tk.LEFT, fill=tk.X, pady=5)
        self.controlPanel.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)


    ##
    # Handles the step button click event.
    # This method runs the simulation for the specified number of steps
    # and updates the chart with the results.
    # @param n: The number of steps to run the simulation.
    def on_step(self, n: int):
        self.simulation.run_simulation(n)
        s, i, r = self.simulation.stats.get_list_report()
        self.chart.plot(s, i, r)

    ##
    # Runs the simulation for a specified number of days.
    # This method calls the simulate_step method of the simulation instance
    # for the given number of days.
    # @param no_days: The number of days to run the simulation.
    # @return: None
    def run_simulation(self, no_days):
        for i in range(no_days):
            self.simulation.simulate_step()

    ##
    # Loads the simulation parameters from the parameter panel.
    # This method retrieves the parameters set by the user in the parameter panel
    # and returns them as a SimulationParameters object.
    # If there is an error in loading the parameters, it prints an error message.
    # @return: A SimulationParameters object containing the loaded parameters,
    def load_parameters(self):
        try:
            params : SimulationParameters = self.paramPanel.get_simulation_parameters()
        except ValueError as e:
            print(f"Error loading parameters: {e}")
            return None

        return params

    ##
    # Resets the visualizer and simulation.
    # This method resets the simulation state, clears the chart,
    # and resets the parameter panel fields to their default values.
    # It is called when the user wants to reset the simulation and start over.
    # @return: None
    def reset_everything(self):
        self.simulation.reset_simulation()
        self.chart.plot([], [], [])
        self.paramPanel.reset_fields()


    ##
    # Starts the simulation with the loaded parameters.
    # This method retrieves the parameters from the parameter panel,
    # sets up the simulation with those parameters, and returns True if successful.
    # If there is an error in setting up the simulation, it prints an error message
    # and returns False.
    # @return: True if the simulation was set up successfully, False otherwise.
    def start_simulation(self):
        params = self.load_parameters()
        try:
            self.simulation.setup_simulation(params)
        except RuntimeError as e:
            print(f"Error loading parameters: {e}")
            return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Disease Simulation Visualizer")

    from simulation import Simulation
    sim = Simulation()

    visualizer = Visualizer(master=root, simulation=sim)

    root.mainloop()