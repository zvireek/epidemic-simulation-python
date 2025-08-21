## @package statstracker
#  Tracks the health status of the population over time.
#  This class records the number of susceptible, infected, and recovered individuals

from models import HealthStatus

class StatsTracker:
    ##
    #  Initialize the StatsTracker with empty histories for each health status.
    def __init__(self):
        self.s_history = []
        self.i_history = []
        self.r_history = []

    ##
    # Record the health status of the population at a given time step.
    # @param time: The current time step in the simulation.
    # @param population: The population object containing persons' data.
    def record_step(self, time, population):
        status_counts = {
            HealthStatus.Susceptible: 0,
            HealthStatus.Infected: 0,
            HealthStatus.Recovered: 0
        }

        for person in population.persons:
            status_counts[person.get_status(time)] += 1

        self.s_history.insert(time, status_counts[HealthStatus.Susceptible])
        self.i_history.insert(time, status_counts[HealthStatus.Infected])
        self.r_history.insert(time, status_counts[HealthStatus.Recovered])

    ##
    # Generate a summary report of the health status history (for plotting).
    # @return A tuple containing three lists: susceptible, infected, and recovered counts over time.
    def get_list_report(self):
        return self.s_history, self.i_history, self.r_history
