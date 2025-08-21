## @package simulation
#  The main simulation class that orchestrates the disease spread simulation.
#  It initializes the population, disease, and policies, and runs the simulation steps.


from models import Disease
from models import Population
from models import SimulationParameters
from models import RandomTransmissionPolicy
from .statstracker import StatsTracker
import random

class Simulation:
    ##
    # Initializes the Simulation class.
    def __init__(
            self
    ):
        self.population = None
        self.disease = None
        self.policy = None
        self.stats = None
        self.current_time = -1


    ##
    # Sets up the simulation with the given parameters.
    # This method initializes the population, disease, and policy based on the provided parameters.
    # It also sets the initial state of the simulation, including patient zero.
    #
    # @param params: SimulationParameters object containing the configuration for the simulation.
    def setup_simulation(self, params : SimulationParameters):
        self.population = Population(params.young_population,
                                     params.middle_population,
                                     params.old_population)

        self.disease = Disease(params.disease_name,
                               params.transmission_rate,
                               params.incubation_period,
                               params.infectious_period)

        self.policy = RandomTransmissionPolicy(self.disease)
        self.stats = StatsTracker()

        # -------------------- Patient Zero ------------------------- #
        # Infect patient zero to start the simulation
        patient_zero = random.choice(self.population.persons)
        # --- Option 1 ---
        patient_zero.infectious_time = 0  # To make the plots more interesting, we keep the patient zero infected at all times
        # --- Option 2 ---
        # self.disease.infect(patient_zero, self.current_time) # Uncomment this line if you want to make patient zero behave like a normal infection
        # ----------------------------------------------------------- #
        self.current_time = 0


    ##
    # Runs the simulation for a specified number of days.
    # This method repeatedly calls simulate_step to advance the simulation.
    # @param no_days: The number of days to run the simulation.
    def run_simulation(self, no_days):
        for i in range(no_days):
            self.simulate_step()


    ##
    # Simulates a single step in the simulation.
    # This method processes each person in the population, checks their infectious status,
    # and attempts to infect others based on their interactions.
    # It updates the current time and records statistics for the day.
    # Raises RuntimeError if the simulation is not set up before calling this method.
    # @return: None
    def simulate_step(self):
        if self.current_time == -1:
            raise RuntimeError("Simulation not set up. Call setup_simulation first.")

        infected_today = [] # List of people infected this day
        for person in self.population.persons:
            if not person.is_infectious(self.current_time):
                continue
            contacts = self.population.get_contacts(person)
            newly_infected = person.interact(self.disease, contacts, self.current_time)
            infected_today += newly_infected

        for person in infected_today:
            if person.should_infect():
                self.disease.infect(person, self.current_time)

        self.current_time += 1
        self.stats.record_step(self.current_time, self.population)

        # --- Uncomment the following lines to see detailed reports (for debugging) ---
        """
        print(f"Simulation step at time {self.current_time} completed.")
        self.population.population_report(self.current_time)
        """


    ##
    # Resets the simulation to its initial state.
    # This method clears the population, disease, policy, and stats,
    # and resets the current time to -1.
    # It is useful for starting a new simulation without having to recreate the Simulation object.
    # @return: None
    def reset_simulation(self):
        """
        Resets the simulation to its initial state.
        :return:
        """
        self.population = None
        self.disease = None
        self.policy = None
        self.stats = None
        self.current_time = -1
        print("Simulation has been reset.")


    ##
    # Toggles social distancing measures in the simulation.
    # This method adjusts the distancing factor for each person in the population.
    # If social distancing is enabled, it increases the distancing factor based on the person's activity level.
    # If social distancing is disabled, it resets the distancing factor to 1.0.
    # Raises RuntimeError if the simulation is not set up before calling this method.
    # @param enable: True to enable social distancing, False to disable.
    def toggle_social_distancing(self, enable: bool):
        if self.population is None:
            raise RuntimeError("Simulation not set up. Call setup_simulation first.")

        for person in self.population.persons:
            if enable:
                person.distancing_factor = 1 / (2 * person.activity_level ** 0.5)  # Take a square root to reduce the distancing factor based on activity level
            else:
                person.distancing_factor = 1.0

