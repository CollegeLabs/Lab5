from src.agents import *
import numpy as np
import random


class UniformCostAgent():
    def __init__(self):
        self.performance = 0

class IterativeDeepeningAStartAgent():
    def __init__(self):
        self.performance = 0

class Ghost():
    def __init__(self, Graph):
        size = len(Graph.nodes())
        power = 0.3
        self.power = power*size