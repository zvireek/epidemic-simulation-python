## @package parameterpanel
#  The parameter panel class that allows users to configure simulation parameters.
#  It provides a user interface for setting population sizes, disease parameters,
#  and other simulation settings. The parameters are validated and can be retrieved
#  as a SimulationParameters object for use in the simulation.
#  If any parameter is invalid, an error message is displayed.
#  If the user presses Enter in a field, it validates the input and disables the field.

from models import SimulationParameters
import tkinter as tk
import tkinter.messagebox as mb


class ParameterPanel(tk.Frame):
    ##
    # Initializes the ParameterPanel class.
    # @param master: The parent widget (usually a Tk root or another Frame).
    def __init__(
            self,
            master: tk.Misc,
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        # Create variables
        self.vars = {
            'young_population': tk.IntVar(value=1000),
            'middle_population': tk.IntVar(value=1000),
            'old_population': tk.IntVar(value=1000),
            'disease_name': tk.StringVar(value="Rumour"),
            'transmission_rate': tk.DoubleVar(value=0.15),
            'incubation_period': tk.IntVar(value=5),
            'infectious_period': tk.IntVar(value=14),
        }

        # Define field order and labels
        self.field_specs = [
            ('Young Population', 'young_population'),
            ('Middle Population', 'middle_population'),
            ('Old Population', 'old_population'),
            ('Disease Name', 'disease_name'),
            ('Transmission Rate', 'transmission_rate'),
            ('Incubation Period', 'incubation_period'),
            ('Infectious Period', 'infectious_period'),
        ]

        # Build UI
        param_frame = tk.Frame(self)
        param_frame.pack(pady=5)

        self.entries = {}
        for row, (label_text, var_name) in enumerate(self.field_specs):
            tk.Label(
                param_frame,
                text=label_text,
                font=('calibre', 10, 'bold')
            ).grid(row=row, column=0, sticky='w', padx=5, pady=5)

            entry = tk.Entry(
                param_frame,
                textvariable=self.vars[var_name],
                font=('calibre', 10, 'normal'),
                width=30
            )
            entry.grid(row=row, column=1, padx=5, pady=5)
            entry.bind('<Return>', self._on_enter)

            self.entries[var_name] = entry

    ##
    # Handles the Enter key event for each entry field.
    # Validates the input, updates the background color, and disables the entry.
    # If the input is invalid, it shows an error message and highlights the field.
    # @param event: The key event triggered by pressing Enter.
    def _on_enter(self, event):
        entry = event.widget
        var_name = next(name for name, e in self.entries.items() if e is entry)
        var = self.vars[var_name]
        # Attempt cast (IntVar/DoubleVar/StringVar will validate automatically)
        try:
            _ = var.get()
        except tk.TclError:
            entry.config(bg='lightcoral')
            mb.showerror('Invalid Input', f"Invalid value for {var_name.replace('_', ' ').title()}")
            return 'break'

        entry.config(bg='white', state='disabled')
        return 'break'


    ##
    # Retrieves the simulation parameters from the entry fields.
    # Validates that all fields are committed (disabled) and returns a SimulationParameters object.
    # If any field is not committed, it shows a warning and raises a ValueError.
    # @return: A SimulationParameters object containing the configured parameters.
    def get_simulation_parameters(self) -> SimulationParameters:
        # Ensure all entries are committed (disabled)
        for var_name, entry in self.entries.items():
            if entry['state'] != 'disabled':
                mb.showwarning('Incomplete', f"Please press Enter in the '{var_name.replace('_', ' ').title()}' field.")
                raise ValueError(f"Field {var_name} not committed")

        # Build SimulationParameters
        try:
            return SimulationParameters(
                young_population=self.vars['young_population'].get(),
                middle_population=self.vars['middle_population'].get(),
                old_population=self.vars['old_population'].get(),
                disease_name=self.vars['disease_name'].get(),
                transmission_rate=self.vars['transmission_rate'].get(),
                incubation_period=self.vars['incubation_period'].get(),
                infectious_period=self.vars['infectious_period'].get(),
            )
        except ValueError as e:
            mb.showerror('Invalid Parameters', str(e))
            raise


    ##
    # Resets all entry fields to their initial values.
    # This method sets the background color to white, enables the entries,
    # and sets the variables to their hardcoded initial values.
    # It also clears any selection in the entries.
    # This is useful for resetting the parameter panel to its default state.
    def reset_fields(self):
        # Reset all entries to their initial values
        # Hardcoded initial values for simplicity
        for var_name, entry in self.entries.items():
            var = self.vars[var_name]
            entry.config(state='normal', bg='white')
            if isinstance(var, tk.IntVar):
                if 'population' in var_name:
                    var.set(1000)
                elif 'incubation_period' in var_name:
                    var.set(5)
                elif 'infectious_period' in var_name:
                    var.set(14)
            elif isinstance(var, tk.DoubleVar):
                var.set(0.15)
            elif isinstance(var, tk.StringVar):
                var.set("Rumour" if 'disease' in var_name else "")
            entry.select_clear()
