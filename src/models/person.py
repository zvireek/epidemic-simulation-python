## @package person
#  Defines an individual in the simulation with health state and behavior.
#
#  This class tracks when a person becomes infectious, when they recover,
#  and whether they are currently able to transmit disease.

from .healthstatus import HealthStatus
import random


class Person:
    ##
    #  Construct a Person.
    #  @param id               Unique identifier for the person.
    #  @param susceptibility   Modifier [0.0–1.0] to scale transmission probability.
    #  @param recovery_time    Simulation day when this person recovers.
    #  @param infectious_time  Simulation day when this person becomes infectious.
    #  @param activity_level   Average number of contacts per day.
    #  @param distancing_factor Factor to reduce contacts due to social distancing.
    def __init__(self,
                 id,
                 susceptibility,
                 recovery_time,
                 infectious_time,
                 activity_level,
                 distancing_factor = 1.0):

        self.id = id
        self.susceptibility = susceptibility
        self.recovery_time = recovery_time
        self.infectious_time = infectious_time
        self.activity_level = activity_level
        self.distancing_factor = distancing_factor


    ##
    #  Process daily contacts with other persons and attempt to infect them.
    #  @param disease         The disease that is being transmitted.
    #  @param others          List of other persons that this person interacts with.
    #  @param time            The current time in the simulation.
    #  @return               List of newly infected persons.
    def interact(self, disease, others, time):
        newly_infected = []
        for other in others:
            if other.id != self.id:
                if other.get_status(time) != HealthStatus.Susceptible:
                    continue
                if disease.attempt_infection(self, other, time):
                    newly_infected.append(other)

        return newly_infected

    ##
    #  Determines if this person should be infected based on their susceptibility.
    #  @return True if the person should be infected, False otherwise.
    def should_infect(self):
        return random.random() <= self.susceptibility


    ##
    #  Returns the health status of this person based on the current time.
    #  The person recovers after the recovery time has passed.
    #  If the person has been recovered for more than 90 days, they become susceptible again.
    #  @param current_time: The current time in the simulation.
    #  @return HealthStatus.Susceptible, HealthStatus.Infected, or HealthStatus.Recovered
    def get_status(self, current_time):
        if current_time < self.infectious_time or self.recovery_time <= current_time - 90:
            return HealthStatus.Susceptible
        elif self.infectious_time <= current_time < self.recovery_time:
            return HealthStatus.Infected
        elif self.recovery_time <= current_time:
            return HealthStatus.Recovered


    ##
    # Returns True if the person is currently infectious.
    # @param current_time: The current time in the simulation.
    # @return True if the person is infectious, False otherwise.
    def is_infectious(self, current_time):
        return self.infectious_time <= current_time < self.recovery_time