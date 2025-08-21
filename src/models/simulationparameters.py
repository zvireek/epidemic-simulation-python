## @package simulationparameters
#  Holds all user-configurable simulation settings.
#
#  This includes population sizes, disease parameters, and other simulation settings.
#  The parameters are used to initialize the simulation and can be modified as needed.


from dataclasses import dataclass

@dataclass
class SimulationParameters:
    young_population: int
    middle_population: int
    old_population: int

    disease_name: str
    transmission_rate: float
    incubation_period: int
    infectious_period: int

    ##
    # Initializes the simulation parameters.
    # @param young_population: Number of young individuals in the population.
    # @param middle_population: Number of middle-aged individuals in the population.
    # @param old_population: Number of old individuals in the population.
    # @param disease_name: Name of the disease being simulated.
    # @param transmission_rate: Controls the likelihood of disease transmission between individuals.
    # @param incubation_period: Duration before an infected individual becomes infectious.
    # @param infectious_period: Duration for which an individual remains infectious.
    def __init__(
            self,
            young_population,
            middle_population,
            old_population,
            disease_name,
            transmission_rate,
            incubation_period,
            infectious_period
    ):
        self.young_population = young_population
        self.middle_population = middle_population
        self.old_population = old_population
        self.disease_name = disease_name
        self.transmission_rate = transmission_rate
        self.incubation_period = incubation_period
        self.infectious_period = infectious_period

        self.__post_init__()

    ##
    # Post-initialization checks to validate the parameters.
    # Raises ValueError if any parameter is invalid.
    def __post_init__(self):
        if self.young_population < 0 or self.middle_population < 0 or self.old_population < 0:
            raise ValueError("Population counts must be non-negative")
        if not self.disease_name or self.disease_name == '':
            raise ValueError("Disease name must be non-empty")
        if not (0.0 <= self.transmission_rate <= 1.0):
            raise ValueError("Transmission rate must be between 0 and 1")
        if self.incubation_period < 0:
            raise ValueError("Incubation period must be at least 1 day")
        if self.infectious_period < 1:
            raise ValueError("Infectious period must be at least 1 day")