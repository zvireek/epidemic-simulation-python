## @package disease
# Defines a disease with its parameters and transmission behavior.


from .healthstatus import HealthStatus
from .policy import TransmissionPolicy, RandomTransmissionPolicy, AlwaysTransmitPolicy
# from person import Person

class Disease:
    ##
    # Set up a Disease object with its parameters and transmission policy.
    # @param name: Name of the disease.
    # @param transmission_rate: Likelihood of disease transmission between individuals.
    # @param incubation_period: Duration before an infected individual becomes infectious.
    # @param infectious_period: Duration for which an individual remains infectious.
    def __init__(self, name, transmission_rate, incubation_period, infectious_period):
        self.name = name
        self.transmission_rate = transmission_rate
        self.infectious_period = infectious_period
        self.incubation_period = incubation_period
        self.policy = RandomTransmissionPolicy(self) # should be editable, is not so far

    ##
    # Attempt to infect a target person based on the disease's transmission rate.
    # @param source: The person attempting to transmit the disease.
    # @param target: The person who may receive the disease.
    # @param time: The current time in the simulation.
    # @return: True if the target should get infected, False otherwise.
    def attempt_infection(self, source, target, time):
        if source.get_status(time) != HealthStatus.Infected:
            return False
        if target.get_status(time) != HealthStatus.Susceptible:
            return False
        if source.susceptibility <= 0:
            return False
        if target.susceptibility <= 0:
            return False

        return self.policy.should_transmit(source, target)

    ##
    # Infect a person with the disease.
    # @param person: The person to be infected.
    # @param time: The current time in the simulation.
    def infect(self, person, time):
        person.infectious_time = time
        person.recovery_time = time + self.incubation_period + self.infectious_period

