## @package healthstatus
#  Defines the health status of individuals in the simulation.
#  This module provides an enumeration for the health status of individuals,
#  including Susceptible, Infected, and Recovered.

from enum import Enum

##
#  Enumeration for the health status of individuals in the simulation.
class HealthStatus(Enum):
    Susceptible = 1
    Infected = 2
    Recovered = 3