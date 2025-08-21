## @package policy
#  Defines transmission policies for disease spread.

import abc
import random

class TransmissionPolicy(abc.ABC):
    def __init__(self, disease):
        self.disease = disease

    ##
    # Abstract method to determine if transmission should occur.
    # @param source: The person attempting to transmit the disease.
    # @param target: The person who may receive the disease.
    @abc.abstractmethod
    def should_transmit(self, source, target):
        pass

    ##
    # Abstract method to get the name of the transmission policy.
    # @return: A string representing the name of the policy.
    @abc.abstractmethod
    def get_policy_name(self):
        pass


##
# RandomTransmissionPolicy implements a random chance of disease transmission.
# It inherits from TransmissionPolicy and overrides the should_transmit method.
# This policy randomly determines whether transmission should occur based on the disease's transmission rate.
class RandomTransmissionPolicy(TransmissionPolicy):
    ##
    # Randomly determines whether transmission should occur based on the disease's transmission rate.
    # @param source: The person attempting to transmit the disease.
    # @param target: The person who may receive the disease.
    # @return: True if transmission occurs, False otherwise.
    def should_transmit(self, source, target):
        return random.random() < self.disease.transmission_rate

    def get_policy_name(self):
        return "Random Transmission Policy"


##
# AlwaysTransmitPolicy implements a policy where transmission always occurs.
# It inherits from TransmissionPolicy and overrides the should_transmit method.
class AlwaysTransmitPolicy(TransmissionPolicy):
    ##
    # Always allows transmission to occur.
    # @param source: The person attempting to transmit the disease.
    # @param target: The person who may receive the disease.
    # @return: True, indicating transmission always occurs.
    def should_transmit(self, source, target):
        return True

    def get_policy_name(self):
        return "Always Transmit Policy"