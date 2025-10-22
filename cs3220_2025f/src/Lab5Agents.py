from src.agents import ProblemSolvingMazeAgentBFS
import numpy as np
import random


class UniformCostAgent():
    def __init__(self):
        self.performance = 0

class IterativeDLSAgent():
    def __init__(self):
        self.performance = 0

class EnemyShip():
    def __init__(self, Graph):
        size = len(Graph.nodes())
        power = round(random.uniform(0.10,0.40), 2)
        self.power = power*size