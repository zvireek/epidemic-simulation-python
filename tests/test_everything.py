

import unittest
import random
import math

from models import (
    SimulationParameters,
    HealthStatus,
    Person,
    RandomTransmissionPolicy,
    AlwaysTransmitPolicy,
    Disease,
    Population
)
from simulation import StatsTracker


class TestSimulationParameters(unittest.TestCase):
    def test_valid_parameters(self):
        sp = SimulationParameters(10, 20, 30, 'Flu', 0.5, 2, 3)
        self.assertEqual(sp.young_population, 10)
        self.assertEqual(sp.middle_population, 20)
        self.assertEqual(sp.old_population, 30)
        self.assertEqual(sp.disease_name, 'Flu')
        self.assertEqual(sp.transmission_rate, 0.5)
        self.assertEqual(sp.incubation_period, 2)
        self.assertEqual(sp.infectious_period, 3)

    def test_invalid_population(self):
        with self.assertRaises(ValueError):
            SimulationParameters(-1, 0, 0, 'A', 0.1, 1, 1)

    def test_invalid_disease_name(self):
        with self.assertRaises(ValueError):
            SimulationParameters(1, 1, 1, '', 0.1, 1, 1)

    def test_invalid_transmission_rate(self):
        for rate in [-0.1, 1.1]:
            with self.assertRaises(ValueError):
                SimulationParameters(1, 1, 1, 'A', rate, 1, 1)

    def test_invalid_periods(self):
        with self.assertRaises(ValueError):
            SimulationParameters(1, 1, 1, 'A', 0.5, -1, 1)
        with self.assertRaises(ValueError):
            SimulationParameters(1, 1, 1, 'A', 0.5, 1, -1.2)


class TestHealthStatus(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(HealthStatus.Susceptible.value, 1)
        self.assertEqual(HealthStatus.Infected.value, 2)
        self.assertEqual(HealthStatus.Recovered.value, 3)


class TestPerson(unittest.TestCase):
    def setUp(self):
        # Recovery at day 10, infectious from day 5
        self.person = Person(id=1, susceptibility=0.5, recovery_time=10, infectious_time=5, activity_level=10)

    def test_get_status_susceptible(self):
        self.assertEqual(self.person.get_status(0), HealthStatus.Susceptible)

    def test_get_status_infected(self):
        self.assertEqual(self.person.get_status(5), HealthStatus.Infected)
        self.assertEqual(self.person.get_status(9), HealthStatus.Infected)

    def test_get_status_recovered(self):
        self.assertEqual(self.person.get_status(10), HealthStatus.Recovered)
        # After 90 days from recovery, becomes susceptible again
        person2 = Person(id=2, susceptibility=0.5, recovery_time=0, infectious_time=0, activity_level=1)
        self.assertEqual(person2.get_status(90), HealthStatus.Susceptible)

    def test_is_infectious(self):
        self.assertFalse(self.person.is_infectious(4))
        self.assertTrue(self.person.is_infectious(5))
        self.assertFalse(self.person.is_infectious(10))


class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.disease = Disease('Test', 0.5, 1, 1)

    def test_random_policy(self):
        policy = RandomTransmissionPolicy(self.disease)
        self.disease.transmission_rate = 0.0
        random.seed(0)
        self.assertFalse(policy.should_transmit(None, None))
        self.disease.transmission_rate = 1.0
        self.assertTrue(policy.should_transmit(None, None))

    def test_always_policy(self):
        policy = AlwaysTransmitPolicy(self.disease)
        for _ in range(5):
            self.assertTrue(policy.should_transmit(None, None))


class TestDisease(unittest.TestCase):
    def setUp(self):
        self.disease = Disease('Test', 0.5, 1, 2)
        # Use deterministic policy
        self.disease.policy = AlwaysTransmitPolicy(self.disease)
        self.source = Person(id=1, susceptibility=0.5, recovery_time=10, infectious_time=0, activity_level=1)
        self.target = Person(id=2, susceptibility=0.5, recovery_time=100, infectious_time=100, activity_level=1)

    def test_attempt_infection_not_infected_source(self):
        # Source not infectious at time -1
        self.source.infectious_time = 5
        self.source.recovery_time = 10
        self.assertFalse(self.disease.attempt_infection(self.source, self.target, 0))

    def test_attempt_infection_not_susceptible_target(self):
        # Target already infected
        self.source.infectious_time = 0
        self.source.recovery_time = 10
        self.target.infectious_time = 0
        self.target.recovery_time = 10
        self.assertFalse(self.disease.attempt_infection(self.source, self.target, 1))

    def test_attempt_infection_successful(self):
        # Valid infection scenario
        self.source.infectious_time = 0
        self.source.recovery_time = 10
        self.target.infectious_time = math.inf
        self.target.recovery_time = math.inf
        self.assertTrue(self.disease.attempt_infection(self.source, self.target, 1))

    def test_infect_sets_times(self):
        person = Person(id=3, susceptibility=0.1, recovery_time=math.inf, infectious_time=math.inf, activity_level=1)
        self.disease.infect(person, time=5)
        expected_recovery = 5 + self.disease.incubation_period + self.disease.infectious_period
        self.assertEqual(person.infectious_time, 5)
        self.assertEqual(person.recovery_time, expected_recovery)


class TestPopulation(unittest.TestCase):
    def test_population_counts(self):
        pop = Population(2, 1, 1)
        self.assertEqual(len(pop.persons), 4)

    def test_get_contacts_no_activity(self):
        pop = Population(1, 0, 0)
        p = pop.persons[0]
        p.activity_level = 0
        p.distancing_factor = 1.0
        self.assertEqual(pop.get_contacts(p), [])

    def test_get_contacts_all(self):
        pop = Population(3, 0, 0)
        p = pop.persons[0]
        p.activity_level = 10
        p.distancing_factor = 10
        contacts = pop.get_contacts(p)
        self.assertEqual(set(contacts), set(pop.persons))


class TestStatsTracker(unittest.TestCase):
    def test_record_and_report(self):
        pop = Population(1, 1, 0)
        tracker = StatsTracker()
        # Initially, all are susceptible
        tracker.record_step(0, pop)
        s_history, i_history, r_history = tracker.get_list_report()
        self.assertEqual(s_history[0], 2)
        self.assertEqual(i_history[0], 0)
        self.assertEqual(r_history[0], 0)


if __name__ == '__main__':
    unittest.main()
