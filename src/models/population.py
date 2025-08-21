## @package population
#  The Population class represents a group of individuals in the simulation.
#  It initializes individuals with varying susceptibility and activity levels based on their age group.


from .person import Person
from .healthstatus import HealthStatus
import random
from math import inf

# --- Susceptibility parameters ---
def young_susc(): return random.uniform(0.1, 0.4)
def middle_susc(): return random.uniform(0.2, 0.7)
def old_susc(): return random.uniform(0.4, 0.95)

# --- Activity level parameters ---
def young_act_lvl(): return random.randint(10, 30)
def middle_act_lvl(): return random.randint(5, 25)
def old_act_lvl(): return random.randint(1, 15)


class Population:
    ##
    # Initializes the Population class.
    # Creates a population of persons with varying susceptibility and activity levels based on age groups.
    # @param young: Number of young persons in the population.
    # @param middle: Number of middle-aged persons in the population.
    # @param old: Number of old persons in the population.
    def __init__(self, young: int = 0, middle: int = 0, old: int = 0):
        self.persons = []

        for i in range(young + middle + old):
            if i < young:
                susc = young_susc
                act_lvl = young_act_lvl
            elif young <= i < middle:
                susc = middle_susc
                act_lvl = middle_act_lvl
            else:
                susc = old_susc
                act_lvl = old_act_lvl

            p = Person(i,
                       susceptibility= susc(),
                       recovery_time = inf,
                       infectious_time = inf,
                       activity_level = act_lvl()
                       )
            self.persons.append(p)

        print(f"Population created with {len(self.persons)} persons: ",
              f"{young} young, {middle} middle-aged, and {old} old persons.")


    ##
    # Prints a detailed report of each person's health status.
    # This method iterates through all persons in the population and prints their details.
    # Mainly used for debugging or detailed analysis.
    def detailed_population_report(self):
        for p in self.persons:
            print(p)


    ##
    # Prints a summary of the population's health status.
    # This method counts the number of persons in each health status category (Susceptible, Infected, Recovered)
    # and prints a report. Similar to the get_list_report method in StatsTracker, but prints directly to the console.
    # @param time: The current time in the simulation, used to determine each person's health status.
    def population_report(self, time):
        status_counts = {
            HealthStatus.Susceptible: 0,
            HealthStatus.Infected: 0,
            HealthStatus.Recovered: 0
        }


        for person in self.persons:
            status_counts[person.get_status(time)] += 1

        print(f"Population Report on day {time}:")
        print(f"Susceptible: {status_counts[HealthStatus.Susceptible]}")
        print(f"Infected: {status_counts[HealthStatus.Infected]}")
        print(f"Recovered: {status_counts[HealthStatus.Recovered]}")


    ##
    # Returns a list of persons that the given person can interact with.
    # The list is based on the person's activity level and distancing factor.
    # @param person: The person for whom to get contacts.
    def get_contacts(self, person: Person):
        if person.activity_level <= 0 or person.distancing_factor <= 0:
            return []
        if person.activity_level * person.distancing_factor > len(self.persons):
            return self.persons
        # Randomly sample persons based on activity level and distancing factor
        return random.sample(self.persons,
                             k = round(person.activity_level * person.distancing_factor))



