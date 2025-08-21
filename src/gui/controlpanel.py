## @package controlpanel
#  The control panel for the simulation, providing buttons to start, step through,
#  reset the simulation, and toggle social distancing.
#  It also manages the state of these buttons based on the simulation status.

import tkinter as tk
from typing import Callable

class ControlPanel(tk.Frame):
    ##
    # Initializes the control panel with buttons for starting the simulation,
    # stepping through the simulation, resetting it, and toggling social distancing.
    # @param master: The main window or parent widget for the control panel.
    # @param start_simulation: A callable to start the simulation.
    # @param on_step: A callable to handle stepping through the simulation.
    # @param reset_simulation: A callable to reset the simulation.
    # @param toggle_social_distancing: A callable to toggle social distancing measures.
    def __init__(
            self,
            master: tk.Misc,
            start_simulation : Callable[[], bool],
            on_step: Callable[[int], None],
            reset_simulation: Callable[[], None],
            toggle_social_distancing: Callable[[], None],
            *args,
            **kwargs
        ):
        super().__init__(master, *args, **kwargs)
        self.on_step = on_step
        self.toggle_social_distancing = toggle_social_distancing

        # --- Start Simulation Button ---
        self.start_btn = tk.Button(
            master=self,
            text="Start Simulation",
            width=20,
            command=lambda: self.activate_buttons_and_start(start_simulation)
        )
        self.start_btn.pack(pady=5)

        # --- Step Buttons ---
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=5)

        for steps in (1, 10, 100):
            btn = tk.Button(master = self.btn_frame,
                            text = f"{steps} Day{'s' if steps > 1 else ''}",
                            width = 10,
                            command = lambda n = steps: self.on_step(n)
                            )
            btn.config(state=tk.DISABLED)  # Initially disable step buttons
            btn.pack(side=tk.LEFT, padx=2)

        # --- Reset Button ---
        self.reset_btn = tk.Button(
            master=self.btn_frame,
            text="Reset",
            width=10,
            command=lambda: self.reset_and_deselect(reset_simulation) # Reset simulation and deselect SD
        )
        self.reset_btn.config(state=tk.DISABLED)  # Initially disable reset button
        self.reset_btn.pack(side=tk.LEFT, padx=2)

        # --- Social Distancing Button ---
        sd = tk.BooleanVar(value=False)  # Variable to track social distancing state
        self.social_distancing_btn = tk.Checkbutton(
            master=self.btn_frame,
            text="Social Distancing",
            width=15,
            variable=sd,  # Use a BooleanVar to track the state
            command=(lambda: self.check_start_and_toggle_sd(sd)),    # Call the toggle function with the current state
            onvalue=True,  # Value when checked
            offvalue=False,  # Value when unchecked
        )
        self.social_distancing_btn.pack(side=tk.LEFT, padx=2)
        self.social_distancing_btn.deselect()


    ##
    # Function to toggle social distancing based on the current state.
    # Raises RuntimeError if the simulation is not set up before calling this method.
    # @param enable: True to enable social distancing, False to disable.
    def check_start_and_toggle_sd(self, sd: tk.BooleanVar):
        try:
            self.toggle_social_distancing(sd.get())
        except RuntimeError:
            self.social_distancing_btn.deselect()


    ##
    # Activates the buttons and starts the simulation.
    # This method calls the start simulation function and disables the start button.
    # It also enables the step buttons for stepping through the simulation.
    # @param start_simulation: A callable to start the simulation.
    # @return: None
    def activate_buttons_and_start(self, start_simulation: Callable[[], None]):
        # Call the start simulation function
        if not start_simulation():
            return

        # Disable the Start Simulation button
        self.start_btn.config(state=tk.DISABLED)

        # Enable the step buttons
        for btn in self.btn_frame.winfo_children():
            if isinstance(btn, tk.Button):
                btn.config(state=tk.NORMAL)


    ##
    # Resets the control panel and deselects the social distancing button.
    # This method resets the simulation state, disables the step buttons,
    # and calls the reset simulation function.
    # @param reset_simulation: A callable to reset the simulation.
    # @return: None
    def reset_and_deselect(self, reset_simulation: Callable[[], None]):
        self.social_distancing_btn.deselect()
        self.start_btn.config(state=tk.NORMAL)

        # Disable step buttons
        for btn in self.btn_frame.winfo_children():
            if isinstance(btn, tk.Button):
                btn.config(state=tk.DISABLED)

        # Call the reset simulation function
        try:
            reset_simulation()
        except RuntimeError as e:
            print(f"Error resetting simulation: {e}")
            return



